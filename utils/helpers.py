def get_language_code(language: str) -> str:

    if language.lower() == "urdu":
        return "ur"

    return "en"


def is_error_message(text: str) -> bool:

    if not text:
        return True

    return text.startswith("ERROR:")