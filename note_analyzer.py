from numpy.lib import average
import sounddevice as sd
import soundfile as sf
from matplotlib import pyplot as plt
import numpy as np


def probability_of_notes(fs, recording_data, min_key=20, max_key=88):
    spectrum = np.abs(np.fft.fft(recording_data))
    spectrum = spectrum[:int(len(spectrum)/2)]
    f = (np.arange(len(spectrum))*fs)/len(recording_data)
    keys_f = np.rint(12*np.log2(f/440)+49).astype(int)
    min_key = max(min_key, keys_f[1])
    max_key = min(max_key, keys_f[-1])
    keys = np.arange(max_key-min_key+1)+min_key
    probability = np.zeros(max_key-min_key+1)
    for i, amplitude in enumerate(spectrum):
        key = keys_f[i]
        if i != 0 and min_key<=key<=max_key:
            probability[np.where(keys==key)[0]] += amplitude
    probability = probability/np.sum(probability)
    return keys, probability

def most_likely_notes(keys, probability, n=3):
    return np.sort(keys[np.argpartition(probability, -n)[-n:]])



if __name__ == "__main__":
    fs = 44100  # Sample rate
    seconds = 0.05  # Duration of recording
    previously_played_keys = []
    while True:
        recording_data = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        recording_data = np.average(recording_data, axis=1)
        recording_data = recording_data/np.max(recording_data)
        keys, probability = probability_of_notes(fs, recording_data)
        average_probability = np.average(probability)
        played_keys = []
        for key, p in zip(keys, probability):
            if p>10*average_probability:
                played_keys.append(note_dict[key])
        if played_keys and played_keys!=previously_played_keys:
            print(played_keys)
        previously_played_keys = played_keys