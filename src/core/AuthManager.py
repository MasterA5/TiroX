import json
import os
from typing import Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TIMEOUT = 15.0


class TiroxAuthManager:
    def __init__(self):
        self.base_url = os.getenv("TIROX_SERVER_URL", "http://localhost:3000")
        self.base_path = os.getenv("FLET_APP_STORAGE_DATA", "./")
        self.__auth_data: dict[str, any] = {}
        self.__load_data_in_local()

    @property
    def __session_file(self) -> str:
        return os.path.join(self.base_path, "session.json")

    def __load_data_in_local(self):
        try:
            if not os.path.exists(self.__session_file):
                return

            with open(self.__session_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict) and data.get("token"):
                self.__auth_data = data
        except (json.JSONDecodeError, OSError):
            return

    def __save_data_in_local(self, data: dict[str, any]):
        try:
            with open(self.__session_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except OSError:
            return

    def __clear_data_in_local(self):
        try:
            if os.path.exists(self.__session_file):
                os.remove(self.__session_file)
        except OSError:
            pass

    def get_current_token(self) -> Optional[str]:
        return self.__auth_data.get("token", None)

    def get_current_user(self) -> Optional[dict]:
        user = self.__auth_data.get("user", None)
        return user if isinstance(user, dict) else None

    def is_auth(self) -> bool:
        return self.get_current_token() is not None

    def auth_headers(self) -> dict:
        token = self.get_current_token()
        if not token:
            return {}
        return {"Authorization": f"Bearer {token}"}

    async def __request(
        self,
        method: str,
        path: str,
        json_body: dict | None = None,
        headers: dict | None = None,
    ) -> Optional[httpx.Response]:
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=DEFAULT_TIMEOUT,
            ) as client:
                return await client.request(
                    method,
                    path,
                    json=json_body,
                    headers=headers or {},
                )
        except httpx.HTTPError:
            return None

    async def login(self, email: str, password: str) -> Optional[dict]:
        res = await self.__request(
            "POST",
            "/api/auth/login",
            json_body={"email": email, "password": password},
        )

        if res is None or res.status_code >= 400:
            return None

        data = res.json()
        if not isinstance(data, dict) or not data.get("token"):
            return None

        self.__auth_data = data
        self.__save_data_in_local(data)
        return data

    async def register(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        age: int | None = None,
    ) -> Optional[dict]:
        res = await self.__request(
            "POST",
            "/api/auth/register",
            json_body={
                "username": username,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
            },
        )

        if res is None or res.status_code >= 400:
            return None

        data = res.json()
        if not isinstance(data, dict) or not data.get("token"):
            # El registro fue exitoso pero sin sesion; intentar login directo.
            return await self.login(email, password)

        self.__auth_data = data
        self.__save_data_in_local(data)
        return data

    async def validate_session(self) -> bool:
        """Valida el token contra el backend. Si expiro o es invalido,
        limpia la sesion local."""
        if not self.is_auth():
            return False

        res = await self.__request("GET", "/api/auth/me", headers=self.auth_headers())

        if res is None:
            # Sin conexion: conservar la sesion en cache.
            return True

        if res.status_code >= 400:
            self.logout()
            return False

        data = res.json()
        if isinstance(data, dict) and isinstance(data.get("user"), dict):
            self.__auth_data["user"] = data["user"]
            self.__save_data_in_local(self.__auth_data)

        return True

    def invalidate_session(self):
        """Fuerza el cierre de sesion (ej. token expirado detectado por el API)."""
        self.__auth_data = {}
        self.__clear_data_in_local()

    def logout(self) -> bool:
        existed = os.path.exists(self.__session_file)
        self.invalidate_session()
        return existed
