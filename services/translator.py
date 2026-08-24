from deep_translator import GoogleTranslator


def translate_to_urdu(text: str) -> str:

    if not text or not text.strip():
        return ""

    try:

        translator = GoogleTranslator(
            source="en",
            target="ur"
        )

        return translator.translate(text)

    except Exception as e:

        print(
            f"English to Urdu translation error: {e}"
        )

        return text


def translate_to_english(text: str) -> str:

    if not text or not text.strip():
        return ""

    try:

        translator = GoogleTranslator(
            source="ur",
            target="en"
        )

        return translator.translate(text)

    except Exception as e:

        print(
            f"Urdu to English translation error: {e}"
        )

        return text


def translate_text(
    text: str,
    source_language: str,
    target_language: str
) -> str:

    if not text or not text.strip():
        return ""

    source_language = source_language.lower()
    target_language = target_language.lower()

    if source_language == target_language:
        return text

    try:

        translator = GoogleTranslator(
            source=source_language,
            target=target_language
        )

        return translator.translate(text)

    except Exception as e:

        print(f"Translation error: {e}")

        return text