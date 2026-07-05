import datetime
import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Register:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    hormone: str = ""
    value: float = 0.0
    notes: str = ""
    date: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self):
        data = asdict(self)
        if isinstance(data["date"], datetime.datetime):
            data["date"] = data["date"].isoformat()
        if isinstance(data["id"], uuid.UUID):
            data["id"] = str(data["id"])
        return data

    @classmethod
    def from_dict(cls, data: dict):
        if "id" in data and isinstance(data["id"], str):
            data["id"] = uuid.UUID(data["id"])
        if "date" in data and isinstance(data["date"], str):
            data["date"] = datetime.datetime.fromisoformat(data["date"])
        if "value" in data and not isinstance(data["value"], float):
            data["value"] = float(data["value"])
        return cls(**data)


class RegisterManager:
    def __init__(self):
        self.registers: list[Register] = []
        self.file_name = self.__get_or_create_file_id()
        self.__load_registers()

    def __get_or_create_file_id(self) -> str:
        registers_path = os.getenv("FLET_APP_STORAGE_DATA", ".")

        meta_file = os.path.join(registers_path, ".register_meta.json")

        if os.path.exists(meta_file):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    if "file_id" in meta:
                        return meta["file_id"]
            except FileNotFoundError:
                pass

        new_file_id = str(uuid.uuid4())

        os.makedirs(registers_path, exist_ok=True)
        try:
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump({"file_id": new_file_id}, f)
        except FileNotFoundError:
            pass

        return new_file_id

    def __save_registers(self):
        registers_path = os.getenv("FLET_APP_STORAGE_DATA", ".")
        os.makedirs(registers_path, exist_ok=True)

        file_path = os.path.join(registers_path, f"{self.file_name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                [register.to_dict() for register in self.registers],
                f,
                indent=4,
                ensure_ascii=False,
            )

    def __load_registers(self):
        registers_path = os.getenv("FLET_APP_STORAGE_DATA", ".")
        file_path = os.path.join(registers_path, f"{self.file_name}.json")

        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.registers = [Register.from_dict(item) for item in data]

        except json.JSONDecodeError as e:
            print(f"Error loading JSON file: {e}")
        except Exception as e:
            print(f"Unexpected error to loading files: {e}")

    def add_register(self, register: Register) -> Optional[Register]:
        if self.get_register_data_by_id(register.id):
            return None

        self.registers.append(register)
        self.__save_registers()
        return register

    def delete_register(self, id: uuid.UUID) -> bool:
        if not id:
            return False

        register = self.get_register_data_by_id(id)
        if not register:
            return False

        self.registers.remove(register)
        self.__save_registers()
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

    def get_last_register(self):
        if not self.registers:
            return None
        return self.registers[-1]
