import pyaudio
import wave
import keyboard
import os
from mega import Mega
import getpass
from datetime import datetime

# Constants
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono channel
RATE = 44100  # Sampling rate
RECORD_SECONDS = 5  # Recording time
MEGA_EMAIL = "your_email@example.com"  # Mega.nz email address
MEGA_PASSWORD = "your_password"  # Mega.nz password

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start recording function
def start_recording():
    print("Recording started...")
    frames = []
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed("f"):
            break
    print("Recording stopped...")

    # Stop the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Get the current user's username
    username = getpass.getuser()

    # Get the current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

    # Save the recorded data as a WAV file
    output_filename = f"{username}_{dt_string}.wav"
    wavefile = wave.open(output_filename, 'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(audio.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    # Upload to Mega.nz
    mega = Mega()
    m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
    file = m.upload(output_filename)
    print("File uploaded to Mega.nz: ", file)

# Press F to start recording
print("Press F to start recording...")
keyboard.wait('f')
start_recording()