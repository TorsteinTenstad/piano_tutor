import numpy as np


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


class Cord(Notes):
    def __init__(self, root_note, intervals):
        super().__init__(root_note, intervals)
        
    def find_name(self):
        for type in intervals_of_named_cords:
            for possible_root in [x for x in self.notes]:
                named_cord = NamedCord(possible_root, type)
                if self == named_cord:
                    return named_cord.name
        return f'Could not find name of cord: {self}'

    def __eq__(self, __o) -> bool:
        return len(self.notes) == len(__o.notes) and (np.sort([x%12 for x in self.notes]) == np.sort([x%12 for x in __o.notes])).all()


intervals_of_named_scales ={'Major': [0, 2, 4, 5, 7, 9, 11],
                            'Minor': [0, 2, 3, 5, 7, 8, 10],
                            'Major Pentatonic': [0, 2, 4, 7, 9],
                            'Minor Pentatonic': [0, 2, 3, 7, 8]}
        
class NamedScale(Scale):
    def __init__(self, root_note, type='Major'):
        intervals = intervals_of_named_scales[type]
        super().__init__(root_note, intervals)

    def get_triad_cord(self, cord_number):
        return Cord(0, [(self.notes + [12 + x for x in self.notes])[cord_number + i] for i in [0, 2, 4]])


intervals_of_named_cords = {'Major': [0, 4, 7],
                            'Minor': [0, 3, 7],
                            'Diminished': [0, 3, 6]}

class NamedCord(Cord):
    def __init__(self, root_note, type='Major'):
        super().__init__(root_note, intervals_of_named_cords[type])
        self.name = f'{note_name[self.notes[0]]} {type}'


if __name__ == '__main__':
    c = Cord('C', [0])
    print(c.find_name())
    scale = NamedScale('A', 'Minor')
    print(scale)
    for i in range(7):
        cord = scale.get_triad_cord(i)
        print(f'{cord.find_name()}: {cord}')