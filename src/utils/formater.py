class Formater:
    @staticmethod
    def format_datetime(datetime: str, legible: bool = False):
        MONTHS = {
            "01": "enero",
            "02": "febrero",
            "03": "marzo",
            "04": "abril",
            "05": "mayo",
            "06": "junio",
            "07": "julio",
            "08": "agosto",
            "09": "septiembre",
            "10": "octubre",
            "11": "noviembre",
            "12": "diciembre",
        }

        if not isinstance(datetime, str):
            return None

        if legible:
            year = datetime.split("T")[0].split(" ")[0].split("-")[0]
            month = MONTHS[datetime.split("T")[0].split(" ")[0].split("-")[1]]
            day = datetime.split("T")[0].split(" ")[0].split("-")[2].replace("0", "")
            hour = datetime.split("T")[0].split(" ")[1].split(".")[0]

            return f"{day} de {month} del {year} a las {hour}"

        formated_datetime = "/".join(
            datetime.split("T")[0].split(" ")[0].split("-")[::-1]
        )

        formated_hour = datetime.split("T")[0].split(" ")[1].split(".")[0]

        return formated_datetime, formated_hour
