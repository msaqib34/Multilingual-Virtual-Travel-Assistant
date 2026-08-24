import speech_recognition as sr

recognizer = sr.Recognizer()

print("Available microphones:")

for index, microphone in enumerate(sr.Microphone.list_microphone_names()):
    print(index, microphone)


print("\nTesting default microphone...")

try:

    with sr.Microphone() as source:

        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Speak now...")

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=10
        )

    print("Converting speech to text...")

    text = recognizer.recognize_google(
        audio,
        language="en-US"
    )

    print("You said:", text)

except Exception as e:

    print("ERROR:")
    print(e)