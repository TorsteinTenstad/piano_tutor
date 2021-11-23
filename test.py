from pygame import midi
import time
from notes_scales_and_cords import note_name_dict


def print_devices():
    for n in range(midi.get_count()):
        print (n, midi.get_device_info(n))


class MidiReader:

    def __init__(self, device_id):
        midi.init()
        self.input_device = midi.Input(device_id)
        self.pressed_keys = []

    def _read_events(self):
        return self.input_device.read(1024)

    def read_played_notes(self):
        events = self._read_events()
        notes = [[event[0][1], event[0][2]] for event in events if event[0][0] == 144]
        for note in notes:
            note_midi_id, preassure = note
            note_number = note_midi_id - 20
            if preassure:
                self.pressed_keys.append(note_number)
            else:
                self.pressed_keys.remove(note_number)
        return notes

    def get_pressed_keys(self):
        self.read_played_notes()
        return self.pressed_keys


if __name__ == '__main__':
    midi_reader = MidiReader(1)
    last_pressed_keys = []
    while True:
        time.sleep(0.3)
        pressed_keys = midi_reader.get_pressed_keys()
        if pressed_keys != last_pressed_keys:
            print([note_name_dict[number] for number in pressed_keys])
        last_pressed_keys = pressed_keys.copy()