import openai
import pyttsx3
import speech_recognition as sr
import time
import apikey;

# Set your Open Api Key
openai.api_key = apikey.apikey
# openai.api_key ="";
# Make sure to hide your api keys, importing it from another file is a good idea

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# This function takes an audio file as input, and returns the transcribed text
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")

# This function generates the responses from openai gtp-3
# The openai api references have a lot to say about making your own 
# https://platform.openai.com/docs/api-reference/making-requests
def generate_response(prompt):
    response = openai.Completion.create(
        # This is the model of open ai, gbt-3
        engine="text-davinci-003",
        prompt=prompt,
        # This is the max number of tokens the api can handle, 4000 is max on the current engine
        max_tokens=4000,
        n=1,
        stop=None,
        # temperature controls the randomness of the ai
        temperature=0.5,
    )
    # This returns the response from the openai bot
    return response["choices"][0]["text"]

# This function will convert the text argument to speech using the pyttsx3
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# This runs the program
def main():
    while True:
        print("Say Genius to start recording your question: ")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="genius":
                    # Starts Recording audio if the word genius is said
                    filename ="input.wav"
                    print("Say your question")
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())

                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says {response}")

                        # Read response using  text-to-speech
                        speak_text(response)
            # This catching errors
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()