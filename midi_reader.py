from pygame import midi
import time
from notes_scales_and_chords import Chord, NamedScale, note_name, note_list, NamedChord, intervals_of_named_chords
import numpy as np
import datetime
from utility_functions import remove_numerics


def print_devices():
    for n in range(midi.get_count()):
        print (n, midi.get_device_info(n))


class MidiReader:

    def __init__(self, device_id):
        midi.init()
        self.input_device = midi.Input(device_id)
        self.rechorded_sequence = []

    def _read_events(self):
        return self.input_device.read(1024)

    def read_played_notes(self):
        events = self._read_events()
        notes = [[event[0][1], event[0][2]] for event in events if event[0][0] == 144]
        for note in notes:
            note_midi_id, preassure = note
            note_number = note_midi_id - 20
            last_state = self.rechorded_sequence[-1].copy() if self.rechorded_sequence else []
            if preassure:
                last_state.append(note_number)
            else:
                try:
                    last_state.remove(note_number)
                except ValueError:
                    pass
            self.rechorded_sequence.append(last_state)
        return notes

    def get_pressed_keys(self):
        self.read_played_notes()
        temp = self.rechorded_sequence
        self.rechorded_sequence = [self.rechorded_sequence[-1]] if self.rechorded_sequence and self.rechorded_sequence[-1] else []
        return temp

    def clear_rechording(self):
        self.rechorded_sequence = []


if __name__ == '__main__':
    midi_reader = MidiReader(1)
    target = generate_random_chord()
    for i in range(50):
        print('')
    print(f'Play {remove_numerics(target.find_name())}')
    start_time = datetime.datetime.now()
    score = 0
    while (datetime.datetime.now()-start_time).seconds < 120:
        time.sleep(0.1)
        pressed_keys = midi_reader.get_pressed_keys()
        for combination in pressed_keys:
            if len(combination) == 3:
                print(f'You played {Chord(0, combination).find_name()}')
                midi_reader.clear_rechording()
            if target == Chord(0, combination):
                score += 1
                print(f'Success! Score: {score}')
                target = generate_random_chord()
                print(f'Play {remove_numerics(target.find_name())}')
                midi_reader.clear_rechording()
    print(f'Time is up! Score: {score}')