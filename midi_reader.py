from pygame import midi
import time
from notes_scales_and_cords import Cord, note_name, note_list, NamedCord, intervals_of_named_cords
import numpy as np
import datetime


def print_devices():
    for n in range(midi.get_count()):
        print (n, midi.get_device_info(n))


class MidiReader:

    def __init__(self, device_id):
        midi.init()
        self.input_device = midi.Input(device_id)
        self.recorded_sequence = []

    def _read_events(self):
        return self.input_device.read(1024)

    def read_played_notes(self):
        events = self._read_events()
        notes = [[event[0][1], event[0][2]] for event in events if event[0][0] == 144]
        for note in notes:
            note_midi_id, preassure = note
            note_number = note_midi_id - 20
            last_state = self.recorded_sequence[-1].copy() if self.recorded_sequence else []
            if preassure:
                last_state.append(note_number)
            else:
                try:
                    last_state.remove(note_number)
                except ValueError:
                    pass
            self.recorded_sequence.append(last_state)
        return notes

    def get_pressed_keys(self):
        self.read_played_notes()
        temp = self.recorded_sequence
        self.recorded_sequence = [self.recorded_sequence[-1]] if self.recorded_sequence and self.recorded_sequence[-1] else []
        return temp

    def clear_recording(self):
        self.recorded_sequence = []


def generate_random_cord():
    root = np.random.choice(note_list)
    cord_type = np.random.choice(list(intervals_of_named_cords))
    return NamedCord(root, cord_type)

def remove_numerics(string):
    return ''.join([c for c in string if not c.isnumeric()])

if __name__ == '__main__':
    midi_reader = MidiReader(1)
    target = generate_random_cord()
    for i in range(50):
        print('')
    print(f'Play {remove_numerics(target.name)}')
    start_time = datetime.datetime.now()
    score = 0
    while (datetime.datetime.now()-start_time).seconds < 60:
        time.sleep(0.1)
        pressed_keys = midi_reader.get_pressed_keys()
        for combination in pressed_keys:
            if len(combination) == 3:
                print(f'You played {Cord(0, combination).find_name()}')
                midi_reader.clear_recording()
            if target == Cord(0, combination):
                score += 1
                print(f'Success! Score: {score}')
                target = generate_random_cord()
                print(f'Play {remove_numerics(target.name)}')
                midi_reader.clear_recording()
    print(f'Time is up! Score: {score}')