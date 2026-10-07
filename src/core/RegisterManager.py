import datetime
import json
import os
import uuid
from dataclasses import asdict, dataclass, field, fields
from typing import Optional

import httpx
from dotenv import load_dotenv

from core.AuthManager import TiroxAuthManager

load_dotenv()

DEFAULT_TIMEOUT = 15.0


@dataclass(frozen=True)
class Register:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    hormone: str = ""
    value: float = 0.0
    notes: str = ""
    date: datetime.datetime = field(default_factory=datetime.datetime.now)
    pending_sync: bool = False

    def to_dict(self):
        data = asdict(self)
        data["date"] = data["date"].isoformat()
        data["id"] = str(data["id"])
        return data

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in valid_keys}

        if isinstance(kwargs.get("id"), str):
            kwargs["id"] = uuid.UUID(kwargs["id"])
        if isinstance(kwargs.get("date"), str):
            kwargs["date"] = datetime.datetime.fromisoformat(kwargs["date"])
        if kwargs.get("value") is not None and not isinstance(kwargs["value"], float):
            kwargs["value"] = float(kwargs["value"])

        return cls(**kwargs)


class RegisterManager:
    def __init__(self, auth_manager: TiroxAuthManager | None = None):
        self.auth_manager = auth_manager
        self.server_url = os.getenv("TIROX_SERVER_URL", "http://localhost:3000")
        self.registers: list[Register] = []
        self.__pending_deletes: list[str] = []
        self.file_name = self.__get_or_create_file_id()
        self.__load_registers()

    # ------------------------------------------------------------------
    # Almacenamiento local
    # ------------------------------------------------------------------

    @property
    def __registers_path(self) -> str:
        return os.getenv("FLET_APP_STORAGE_DATA", ".")

    @property
    def __meta_file(self) -> str:
        return os.path.join(self.__registers_path, ".register_meta.json")

    def __get_or_create_file_id(self) -> str:
        registers_path = self.__registers_path
        os.makedirs(registers_path, exist_ok=True)

        meta = {}
        if os.path.exists(self.__meta_file):
            try:
                with open(self.__meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except (json.JSONDecodeError, OSError):
                meta = {}

        if isinstance(meta, dict) and meta.get("file_id"):
            self.__pending_deletes = [
                str(item) for item in meta.get("pending_deletes", []) if item
            ]
            return meta["file_id"]

        new_file_id = str(uuid.uuid4())
        self.__write_meta({"file_id": new_file_id, "pending_deletes": []})
        self.__pending_deletes = []
        return new_file_id

    def __write_meta(self, meta: dict):
        try:
            with open(self.__meta_file, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=4)
        except OSError:
            pass

    def __save_meta(self):
        self.__write_meta(
            {
                "file_id": self.file_name,
                "pending_deletes": self.__pending_deletes,
            }
        )

    def __save_registers(self):
        registers_path = self.__registers_path
        os.makedirs(registers_path, exist_ok=True)

        file_path = os.path.join(registers_path, f"{self.file_name}.json")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    [register.to_dict() for register in self.registers],
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
        except OSError as e:
            print(f"Error saving registers: {e}")

    def __load_registers(self):
        file_path = os.path.join(self.__registers_path, f"{self.file_name}.json")

        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.registers = [Register.from_dict(item) for item in data]

        except json.JSONDecodeError as e:
            print(f"Error loading JSON file: {e}")
        except (OSError, ValueError, TypeError) as e:
            print(f"Unexpected error to loading files: {e}")

    # ------------------------------------------------------------------
    # Helpers del servidor
    # ------------------------------------------------------------------

    def __auth_headers(self) -> dict:
        if self.auth_manager is None:
            return {}
        return self.auth_manager.auth_headers()

    async def __request(
        self,
        method: str,
        path: str,
        json_body: dict | None = None,
    ) -> Optional[httpx.Response]:
        try:
            async with httpx.AsyncClient(
                base_url=self.server_url,
                timeout=DEFAULT_TIMEOUT,
            ) as client:
                return await client.request(
                    method,
                    path,
                    json=json_body,
                    headers=self.__auth_headers(),
                )
        except httpx.HTTPError:
            return None

    def __handle_auth_error(self, res: Optional[httpx.Response]) -> bool:
        """Invalida la sesion si el backend rechazo el token."""
        if res is not None and res.status_code == 401 and self.auth_manager:
            self.auth_manager.invalidate_session()
            return True
        return False

    @staticmethod
    def __parse_server_date(value) -> datetime.datetime:
        if not value:
            return datetime.datetime.now()
        try:
            parsed = datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            if parsed.tzinfo is not None:
                parsed = parsed.replace(tzinfo=None)
            return parsed
        except ValueError:
            return datetime.datetime.now()

    def __register_from_server(self, data: dict) -> Optional[Register]:
        try:
            return Register(
                id=uuid.UUID(str(data["id"])),
                hormone=str(data.get("hormone", "")),
                value=float(data.get("result", 0.0)),
                notes=data.get("notes") or "",
                date=self.__parse_server_date(data.get("created_at")),
                pending_sync=False,
            )
        except (KeyError, ValueError, TypeError) as e:
            print(f"Invalid record from server: {e}")
            return None

    async def __push_pending_register(self, register: Register) -> Optional[Register]:
        res = await self.__request(
            "POST",
            "/api/records",
            json_body={
                "hormone": register.hormone,
                "result": register.value,
                "notes": register.notes or None,
            },
        )

        if res is not None and res.status_code == 201:
            return self.__register_from_server(res.json())

        self.__handle_auth_error(res)
        return None

    async def __delete_on_server(self, register_id: uuid.UUID) -> bool:
        """Elimina en el servidor. False solo si hay que reintentar
        (fallo de red, token invalido o error del servidor)."""
        res = await self.__request("DELETE", f"/api/records/{register_id}")

        if res is None:
            return False

        if res.status_code in (200, 404):
            return True

        self.__handle_auth_error(res)
        return False

    # ------------------------------------------------------------------
    # API publica (usada por las vistas)
    # ------------------------------------------------------------------

    async def sync_with_server(self) -> bool:
        """Sincroniza con el servidor: baja registros, sube pendientes y
        aplica borrados pendientes. El servidor manda; lo local no sincronizado
        se conserva hasta poder subirlo."""
        if self.auth_manager is None or not self.auth_manager.is_auth():
            return False

        res = await self.__request("GET", "/api/records")
        if res is None:
            return False

        if res.status_code >= 400:
            self.__handle_auth_error(res)
            return False

        payload = res.json()
        server_registers: list[Register] = []
        for item in payload if isinstance(payload, list) else []:
            register = self.__register_from_server(item)
            if register is not None:
                server_registers.append(register)

        # Subir registros locales pendientes.
        still_pending: list[Register] = []
        for register in self.registers:
            if not register.pending_sync:
                continue
            uploaded = await self.__push_pending_register(register)
            if uploaded is None:
                still_pending.append(register)
            else:
                server_registers.append(uploaded)

        # Aplicar borrados que quedaron pendientes por falta de conexion.
        remaining_tombstones: list[str] = []
        for register_id in self.__pending_deletes:
            deleted = await self.__delete_on_server(uuid.UUID(register_id))
            if not deleted:
                remaining_tombstones.append(register_id)
        self.__pending_deletes = remaining_tombstones

        # Filtrar tumbas de los datos del servidor.
        if self.__pending_deletes:
            tombstones = {uuid.UUID(item) for item in self.__pending_deletes}
            server_registers = [r for r in server_registers if r.id not in tombstones]

        server_registers.sort(key=lambda r: r.date)
        self.registers = server_registers + still_pending
        self.__save_registers()
        self.__save_meta()
        return True

    async def create_register(
        self,
        hormone: str,
        value: float,
        notes: str = "",
    ) -> Optional[Register]:
        """Crea un registro priorizando el servidor; si no hay conexion se
        guarda localmente marcado como pendiente de sincronizar."""
        local_register = Register(
            hormone=hormone,
            value=value,
            notes=notes,
        )

        authenticated = self.auth_manager is not None and self.auth_manager.is_auth()

        if authenticated:
            uploaded = await self.__push_pending_register(local_register)
            if uploaded is not None:
                self.registers.append(uploaded)
                self.__save_registers()
                return uploaded

        self.registers.append(
            Register(
                id=local_register.id,
                hormone=local_register.hormone,
                value=local_register.value,
                notes=local_register.notes,
                date=local_register.date,
                pending_sync=True,
            )
        )
        self.__save_registers()
        return self.registers[-1]

    async def delete_register(self, id: uuid.UUID) -> bool:
        if not id:
            return False

        register = self.get_register_data_by_id(id)
        if not register:
            return False

        needs_remote_delete = (
            not register.pending_sync
            and self.auth_manager is not None
            and self.auth_manager.is_auth()
        )

        remote_deleted = True
        if needs_remote_delete:
            remote_deleted = await self.__delete_on_server(id)

        self.registers.remove(register)
        self.__save_registers()

        if needs_remote_delete and not remote_deleted:
            self.__pending_deletes.append(str(id))
            self.__save_meta()

        return True

    def get_register_data_by_id(self, id: uuid.UUID) -> Optional[Register]:
        if not id:
            return None

        for register in self.registers:
            if register.id == id:
                return register

        return None

    def get_all_registers(self) -> list[Register]:
        return [register for register in self.registers]

    def clear_all_registers(self):
        self.registers.clear()
        self.__save_registers()

    def get_last_register(self) -> Optional[Register]:
        ordered = sorted(self.registers, key=lambda r: r.date)
        if not ordered:
            return None
        return ordered[-1]
