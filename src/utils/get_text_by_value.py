def get_text_by_value(value: float | int | str, texts: list[str] | None = None):
    if not texts:
        texts = ["Normal", "Limite Alto", "Alto"]

    tag_text = ""

    if value > 0 and value < 4:
        tag_text = texts[0]
    elif value > 4 and value <= 6:
        tag_text = texts[1]
    elif value > 6:
        tag_text = texts[2]
    else:
        return "No Hay Resultados Para Comparar"

    return tag_text
