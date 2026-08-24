import streamlit as st
import datetime
from audio_recorder_streamlit import audio_recorder

from services.speech_to_text import speech_to_text
from services.translator import translate_text
from services.travel_assistant import generate_travel_response
from services.text_to_speech import text_to_speech

from utils.helpers import (
    get_language_code,
    is_error_message
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Multilingual Travel Assistant",
    page_icon="🌐",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title(" Multilingual Travel Assistant")

st.write(
    "Ask travel questions in English or Urdu "
    "using text or your microphone."
)


# ============================================================
# LANGUAGE
# ============================================================

language = st.selectbox(
    "Select your language",
    [
        "English",
        "Urdu"
    ]
)


language_code = get_language_code(language)


# ============================================================
# INPUT MODE
# ============================================================

input_mode = st.radio(
    "Input Mode",
    [
        "Text",
        "Microphone"
    ],
    horizontal=True
)


# ============================================================
# USER INPUT
# ============================================================

user_input = ""


# ============================================================
# TEXT MODE
# ============================================================

if input_mode == "Text":

    user_input = st.text_area(
        "Enter your travel question:",
        placeholder=(
            "Example: What are the best places to visit in Islamabad?"
            if language == "English"
            else
            "مثال:اسلام آباد  میں گھومنے کے لیے بہترین مقامات کون سے ہیں؟"
        ),
        height=120
    )


# ============================================================
# MICROPHONE MODE
# ============================================================

else:

    st.info(
        "Click the microphone button, speak your question, "
        "and click it again when finished."
    )

    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x"
    )

    if audio_bytes:

        st.audio(
            audio_bytes,
            format="audio/wav"
        )

        with st.spinner(
            f"Converting your {language} speech to text..."
        ):

            user_input = speech_to_text(
                audio_bytes=audio_bytes,
                language=language
            )

        if is_error_message(user_input):

            st.error(user_input)

            user_input = ""

        else:

            st.success("Speech recognized!")

            st.write("### You said:")

            st.write(user_input)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button(
    "🌍 Ask Travel Assistant",
    type="primary",
    use_container_width=True
):

    if not user_input.strip():

        st.warning(
            "Please enter a question or record your voice."
        )

    else:

        # ----------------------------------------------------
        # ORIGINAL QUESTION
        # ----------------------------------------------------

        st.write("### Your Question")

        st.write(user_input)


        # ----------------------------------------------------
        # URDU → ENGLISH
        # ----------------------------------------------------

        if language == "Urdu":

            with st.spinner(
                "Translating Urdu → English..."
            ):

                english_query = translate_text(
                    text=user_input,
                    source_language="ur",
                    target_language="en"
                )

            st.write("### English Translation")

            st.write(english_query)

        else:

            english_query = user_input


        # ----------------------------------------------------
        # GEMINI TRAVEL ASSISTANT
        # ----------------------------------------------------

        with st.spinner(
            "Generating travel response..."
        ):

            english_response = generate_travel_response(
                query=english_query,
                language="English"
            )


        # ----------------------------------------------------
        # ENGLISH → URDU
        # ----------------------------------------------------

        if language == "Urdu":

            with st.spinner(
                "Translating English → Urdu..."
            ):

                final_response = translate_text(
                    text=english_response,
                    source_language="en",
                    target_language="ur"
                )

        else:

            final_response = english_response


        # ----------------------------------------------------
        # DISPLAY RESPONSE
        # ----------------------------------------------------

        st.write("###  Travel Assistant")

        st.markdown(final_response)


        # ----------------------------------------------------
        # TEXT → SPEECH
        # ----------------------------------------------------

        with st.spinner(
            "Preparing audio..."
        ):

            audio_file = text_to_speech(
                text=final_response,
                language=language_code
            )


        if audio_file:

            st.audio(
                audio_file,
                format="audio/mp3"
            )

# --- Sticky Copyright Footer ---
current_year = datetime.datetime.now().year
footer_html = f"""
<style>
.footer {{
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: #888888;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    letter-spacing: 0.5px;
}}
</style>
<div class="footer">
    <p>© {current_year} Muhammad Saqib Ijaz</p>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)         