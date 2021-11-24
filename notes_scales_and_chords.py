import numpy as np
import utility_functions
from matplotlib import pyplot as plt


note_list = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def create_number_name_conversion_dictionaries():
    note_name = {}
    note_number = {}
    for number, name in enumerate(note_list):
        valid_names = [name] + name.split('/')
        for valid_name in valid_names:
            note_number[valid_name] = number + 40
    n = -8
    for o in range(9):
        for x in note_list:
            sharp_and_flat_name = [x + str(o) for x in x.split('/')]
            combined_name = '/'.join(sharp_and_flat_name)
            note_name[n] = combined_name
            note_number[combined_name] = n
            if len(sharp_and_flat_name) > 1:
                note_number[sharp_and_flat_name[0]] = n
                note_number[sharp_and_flat_name[1]] = n
            n += 1
    return note_name, note_number

note_name, note_number = create_number_name_conversion_dictionaries()

def to_note_number(note):
    if isinstance(note, int):
        return note
    elif isinstance(note, str):
        return note_number[note]


class Note:
    def __init__(self, note):
        self.note = to_note_number(note)

    def __repr__(self):
        return note_name[self.note]

    def __add__(self, halfnotes: int):
        return Note(self.note + halfnotes)


class Notes:
    def __init__(self, root_note, intervals):
        root_note = to_note_number(root_note)
        self.notes = [root_note + i for i in intervals]

    def __repr__(self):
        return str([note_name[x] for x in np.sort(self.notes)])


class Scale(Notes):
    def __init__(self, root_note, intervals):
        super().__init__(root_note, intervals)


class Chord(Notes):
    def __init__(self, root_note, intervals):
        super().__init__(root_note, intervals)
        
    def find_name(self):
        for quality in intervals_of_named_chords:
            for possible_root in [x for x in self.notes]:
                named_chord = NamedChord(possible_root, quality)
                if self == named_chord:
                    return named_chord.name
        return str(self)

    def __eq__(self, __o) -> bool:
        return len(self.notes) == len(__o.notes) and (np.sort([x%12 for x in self.notes]) == np.sort([x%12 for x in __o.notes])).all()


intervals_of_named_scales ={'Major': [0, 2, 4, 5, 7, 9, 11],
                            'Minor': [0, 2, 3, 5, 7, 8, 10],
                            'Major Pentatonic': [0, 2, 4, 7, 9],
                            'Minor Pentatonic': [0, 2, 3, 7, 8]}
        
class NamedScale(Scale):
    def __init__(self, root_note, quality='Major'):
        intervals = intervals_of_named_scales[quality]
        super().__init__(root_note, intervals)

    def get_triad_chord(self, chord_number):
        return Chord(0, [(self.notes + [12 + x for x in self.notes])[chord_number + i] for i in [0, 2, 4]])


intervals_of_named_chords = {'maj': [0, 4, 7],
                            'min': [0, 3, 7],
                            'dim': [0, 3, 6]}

class NamedChord(Chord):
    def __init__(self, root_note, quality='maj'):
        super().__init__(root_note, intervals_of_named_chords[quality])
        self.name = f'{note_name[self.notes[0]]}{quality}'


def generate_random_chord():
    root = np.random.choice(note_list)
    chord_type = np.random.choice(list(intervals_of_named_chords))
    return NamedChord(root, chord_type)

if __name__ == '__main__':
    chords = [f'{x} {chord_type}' for x in note_list for chord_type in intervals_of_named_chords]
    chord_to_index = {chord: i for i, chord in enumerate(chords)}
    print(chords)
    scales = [[0.2 if (i//3)%2 else 0 for i, chord in enumerate(chords)] for note in note_list]
    for i, root in enumerate(note_list):
        scale = NamedScale(root, 'Major')
        for j in range(1, 8):
            chord = scale.get_triad_chord(j)
            name = utility_functions.remove_numerics(chord.find_name())
            id = chord_to_index[name]
            scales[i][id] = 1
    plt.imshow(np.array(scales), cmap='gray')
    plt.show()