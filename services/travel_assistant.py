from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS,
    TRAVEL_SYSTEM_PROMPT
)


def generate_travel_response(
    query: str,
    language: str = "English"
) -> str:

    if not GEMINI_API_KEY:

        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to your .env file."
        )

    if not query or not query.strip():

        return "Please enter a travel question."

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=f"""
Answer the following travel question in {language}:

{query}
""",

            config=types.GenerateContentConfig(

                system_instruction=TRAVEL_SYSTEM_PROMPT,

                max_output_tokens=MAX_OUTPUT_TOKENS,

                temperature=0.7
            )
        )

        if response.text:

            return response.text.strip()

        return (
            "Sorry, I could not generate a response."
        )

    except Exception as e:

        print(f"Gemini error: {e}")

        return (
            "Sorry, there was an error while generating "
            f"the travel response: {e}"
        )