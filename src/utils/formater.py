class Formater:
    @staticmethod
    def format_datetime(datetime: str):
        if not isinstance(datetime, str):
            return None

        return '/'.join(datetime.split("T")[0].split(" ")[0].split("-")[::-1])