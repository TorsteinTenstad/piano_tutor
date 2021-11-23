import numpy as np


MAJOR = 'Major'
MINOR = 'Minor'


def create_number_name_conversion_dictionaries():
    note_list = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    note_name = {}
    note_number = {}
    for number, name in enumerate(note_list):
        valid_names = [name] + name.split('/')
        for valid_name in valid_names:
            note_number[valid_name] = number + 40
    n = -8
    for o in range(9):
        for i, x in enumerate(note_list):
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


class Note:

    def __init__(self, note):
        if isinstance(note, int):
            self.number = note
        elif isinstance(note, str):
            self.number = note_number[note]

    def __repr__(self):
        return note_name[self.number]

    def __add__(self, halfnotes: int):
        return Note(self.number + halfnotes)

class Notes:
    def __init__(self, root_note, intervals):
        self.root_note = Note(root_note).number
        self.intervals = intervals

    def __repr__(self):
        return str([Note(self.root_note + i) for i in self.intervals])

class Scale(Notes):
    def __init__(self, root_note, intervals):
        super().__init__(root_note, intervals)
    
    def __getitem__(self, key):
        key = key
        n = len(self.intervals)
        octave = key//n
        return self.intervals[key%n] + 12*octave

class Cord(Notes):
    def __init__(self, root_note, intervals):
        super().__init__(root_note, intervals)
        
    def name(self):
        for cls in [MajorTriad, MinorTriad, DiminishedTriad]:
            for possible_root in [self.root_note + x for x in self.intervals]:
                if self == cls(possible_root):
                    return cls(possible_root).name()
        return 'Could not find name of cord: ' + str(self)

    def __eq__(self, __o) -> bool:
        return (np.sort([(self.root_note + x)%12 for x in self.intervals]) == np.sort([(__o.root_note + x)%12 for x in __o.intervals])).all()

class NatrualScale(Scale):
    def __init__(self, root_note, major_or_minor=MAJOR):
        if major_or_minor == MAJOR:
            super().__init__(root_note, [0, 2, 4, 5, 7, 9, 11])
        if major_or_minor == MINOR:
            super().__init__(root_note, [0, 2, 3, 5, 7, 8, 10])

    def get_triad_cord(self, cord_number):
        return Cord(self.root_note + self[cord_number], [self[cord_number + i] - self[cord_number] for i in [0, 2, 4]])

class PentationicScale(Scale):
    def __init__(self, root_note, major_or_minor=MAJOR):
        corresponding_natural_scale = NatrualScale(root_note, major_or_minor)
        super().__init__(corresponding_natural_scale.root_note, [x for i, x in enumerate(corresponding_natural_scale.intervals) if i+1 not in [4, 7]])

class MajorTriad(Cord):
    def __init__(self, root_note):
            super().__init__(root_note, [0, 4, 7])

    def name(self):
        return f'{Note(self.root_note)} Major'

class MinorTriad(Cord):
    def __init__(self, root_note):
            super().__init__(root_note, [0, 3, 7])

    def name(self):
        return f'{Note(self.root_note)} Minor'

class DiminishedTriad(Cord):
    def __init__(self, root_note):
        super().__init__(root_note, [0, 3, 6])

    def name(self):
        return f'{Note(self.root_note)} Diminished'


if __name__ == '__main__':
    c_major = Cord('C', [0, 4, 7])
    c_major_inverted = Cord('E', [-4, 0, 3])
    print(c_major_inverted.name())
    scale = NatrualScale('A', MINOR)
    print(scale)
    for i in range(7):
        cord = scale.get_triad_cord(i)
        print(f'{cord.name()}: {cord}')