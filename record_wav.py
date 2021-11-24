import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 1  # Duration of rechording

myrechording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until rechording is finished
write('rechording.wav', fs, myrechording)  # Save as WAV file 