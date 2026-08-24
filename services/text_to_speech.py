from gtts import gTTS

import tempfile


def text_to_speech(
    text: str,
    language: str = "en"
):

    if not text or not text.strip():
        return None

    try:

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        temp_file.close()

        tts.save(temp_file.name)

        return temp_file.name

    except Exception as e:

        print(
            f"Text-to-speech error: {e}"
        )

        return None