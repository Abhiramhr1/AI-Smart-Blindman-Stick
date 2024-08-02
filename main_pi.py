#software serial

# import RPi.GPIO as GPIO
import requests
from geopy.distance import geodesic
import time
import serial
import pynmea2
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
import os
import threading

# Define GPIO pin numbers for software serial communication
# RX_PIN = 15  # GPIO pin 23 for receiving data
# TX_PIN = 14  # GPIO pin 24 for transmitting data

KEYWORDS = {
    "car": "01100011",  # Corresponding ASCII: 'c'
    "human": "01101000", # Corresponding ASCII: 'h'
    "person": "01110000", # Corresponding ASCII: 'p'
    "bike": "01100010", # Corresponding ASCII: 'b'
    "barrier": "01100001", # Corresponding ASCII: 'a'
    "object": "01101111"
}
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(RX_PIN, GPIO.IN)
# GPIO.setup(TX_PIN, GPIO.OUT)

# Define software serial port settings
baudrate = 9600

# Replace 'YOUR_API_KEY' with your actual TomTom API key
api_key = 'USSuJvy06RQmZlRcCZueWea21Ht1dkQn'

seconds = 5  # seconds
fs = 44100  # sample rate
output_file = 'output.mp3'


def record_audio():
    # Record audio from default input (Bluetooth earphones)
    print("Recording from Bluetooth earphones...")
    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()

    # Save the recorded audio directly to an MP3 file
    print("Saving audio as MP3...")
    sf.write('output.wav', my_recording, fs)
    sound = AudioSegment.from_wav('output.wav')
    sound.export(output_file, format="mp3")

    print(f"Audio saved to {output_file}")

    speech_text = voicetotext(output_file)
    texttovoice(speech_text)
    return speech_text


def voicetotext(source_file):
    r = sr.Recognizer()
    with sr.AudioFile(source_file) as audio_file:
        audio_data = r.record(audio_file)
    try:
        speech_txt = r.recognize_google(audio_data, language='en')
        print(speech_txt)
        if speech_txt == 'exit':
            exit()
    except sr.UnknownValueError:
        print("Didn't understand the audio")
        texttovoice("Didn't understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        texttovoice("Could not request results from Google Speech Recognition service")
    return speech_txt


def play_audio(source):
    # Play MP3 audio
    print("Playing audio...")
    sd.play('output.wav', fs)
    sd.play(source,fs)
    sd.wait()

    print("Audio playback complete.")


def texttovoice(text):
    try:
        voice = gTTS(text, lang='en')
        voice_path = "voice.mp3"
        voice.save(voice_path)
        play_audio("voice.mp3")
        time.sleep(1)
        os.remove(voice_path)
    except Exception as e:
        print("Text-to-speech error:", e)


def get_coordinates(destination_name, api_key):
    url = f"https://api.tomtom.com/search/2/geocode/{destination_name}.json"
    params = {
        "key": api_key,
        "countrySet": "IN"  # Set to 'IN' for India
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("results"):
        coordinates = data["results"][0]["position"] 
        return coordinates
    else:
        return None


def parse_nmea_sentence(sentence):
    try:
        parsed_sentence = pynmea2.parse(sentence)
        if isinstance(parsed_sentence, pynmea2.RMC):
            latitude = parsed_sentence.latitude
            longitude = parsed_sentence.longitude
            speed = parsed_sentence.spd_over_grnd
            return latitude, longitude, speed
    except pynmea2.ParseError as e:
        print("Error parsing NMEA sentence:", e)
    return None, None, None


def calculate_direction(origin, destination):
    rate = 0.7
    response = requests.get(
        f'https://api.tomtom.com/routing/1/calculateRoute/{origin}:{destination}/json?key={api_key}')
    if response.status_code == 200:
        data = response.json()
        points = data['routes'][0]['legs'][0]['points']
        direction_printed = False
        for i in range(len(points) - 1):
            distance_to_next_point = geodesic((points[i]['latitude'], points[i]['longitude']),
                                              (points[i + 1]['latitude'], points[i + 1]['longitude'])).meters
            lat_diff = points[i + 1]['latitude'] - points[i]['latitude']
            lon_diff = points[i + 1]['longitude'] - points[i]['longitude']
            if lon_diff > 0:
                direction = "right"
            elif lon_diff < 0:
                direction = "left"
            elif lat_diff > 0:
                direction = "straight"
            elif lat_diff < 0:
                direction = "back"
            if (i == 0 or distance_to_next_point <= 5) and not direction_printed:
                if direction != "north" and direction != "south":
                    print(
                        f"At {points[i + 1]['latitude']},{points[i + 1]['longitude']}, turn {direction} in {distance_to_next_point} meters")
                    voicetotext(f" turn {direction} in {distance_to_next_point} meters")
                elif direction == "north":
                    print(
                        f"At {points[i + 1]['latitude']},{points[i + 1]['longitude']}, go straight for {distance_to_next_point} meters")
                    voicetotext(f" turn {direction} in {distance_to_next_point} meters")
                elif direction == "south":
                    print(
                        f"At {points[i + 1]['latitude']},{points[i + 1]['longitude']}, go back for {distance_to_next_point} meters")
                    voicetotext(f" turn {direction} in {distance_to_next_point} meters")
                direction_printed = True
                time.sleep(distance_to_next_point/rate)  # Adjust sleep time as needed
                break
    else:
        print("Error:", response.status_code)


def main():
    # Serial port and other configurations
    port = "/dev/serial0"
    baudrate = 9600

    # Record audio input from the user
    record_audio()#7, "record.wav"

    # Recognize speech from the recorded audio
    texttovoice("say out destination name")
    speech_text = voicetotext("record.wav")

    # Output recognized speech as voice
    texttovoice(speech_text)

    # Use recognized destination name to retrieve coordinates
    destination_name = speech_text
    destination_coordinates = get_coordinates(destination_name, api_key)

    # Check if destination coordinates are found
    if destination_coordinates:
        print("Destination coordinates:", destination_coordinates)
    else:
        print("Destination coordinates not found")
        texttovoice("Destination coordinates not found")
        return


    # Start a separate thread for continuously checking signals
    signal_thread = threading.Thread(target=signal_checker)
    signal_thread.daemon = True  # Set the thread as daemon so it terminates when the main program terminates
    signal_thread.start()
    # Open serial port for GPS data reception
    try:
        with serial.Serial(port, baudrate, timeout=0.5) as ser:
            print("Serial port opened successfully")
            while True:
                sentence = ser.readline().decode('latin-1').strip()
                print("Received:", sentence)
                latitude, longitude, speed = parse_nmea_sentence(sentence)
                if latitude is not None and longitude is not None:
                    print("Latitude:", latitude)
                    print("Longitude:", longitude)
                    print("Speed (knots):", speed)
                    # Calculate and announce the direction to the destination
                    calculate_direction(f"{latitude},{longitude}", f"{destination_coordinates['lat']},{destination_coordinates['lon']}")
    except serial.SerialException as e:
        print("Error opening serial port:", e)
    except KeyboardInterrupt:
        print("Exiting...")

# Call the main function
if __name__ == "__main__":
    main()

