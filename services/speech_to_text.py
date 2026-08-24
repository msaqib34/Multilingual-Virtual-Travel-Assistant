import tempfile
import os

from google import genai
from google.genai import types

from config import GEMINI_API_KEY


def speech_to_text(
    audio_bytes: bytes,
    language: str = "English"
) -> str:
    """
    Convert browser-recorded audio into text using Gemini.

    No PyAudio is required.
    """

    if not GEMINI_API_KEY:
        return (
            "ERROR: Gemini API key is not configured."
        )

    if not audio_bytes:
        return (
            "ERROR: No audio was recorded."
        )

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        # Save browser audio temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_audio:

            temp_audio.write(audio_bytes)

            audio_path = temp_audio.name

        try:

            # Read audio
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()

            prompt = f"""
Listen carefully to this audio recording and convert
the speech into text.

The expected spoken language is {language}.

If the speaker is speaking Urdu, write the transcription
in Urdu script.

If the speaker is speaking English, write the transcription
in English.

Return ONLY the transcription.
Do not explain anything.
Do not translate the speech.
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    types.Part.from_bytes(
                        data=audio_data,
                        mime_type="audio/wav"
                    ),
                    prompt
                ]
            )

            if response.text:
                return response.text.strip()

            return (
                "ERROR: Gemini could not transcribe the audio."
            )

        finally:

            if os.path.exists(audio_path):
                os.remove(audio_path)

    except Exception as e:

        print(f"Speech-to-text error: {e}")

        return f"ERROR: Speech recognition failed: {e}"