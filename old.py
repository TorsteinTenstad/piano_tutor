def note_number_to_name(number: int):
    number = number - 1
    octave_number = number/12
    return ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B'][number % 12]

def note_name_to_number(name: str):
    for note_number in range(12):
        note_name = note_number_to_name(note_number)
        if name in [note_name] + note_name.split('/'):
            return note_number

def note_to_number(note):
    if isinstance(note, int):
        return note
    elif isinstance(note, str):
        return note_name_to_number(note)

def notes_halftones_from_root(root_note, halftones):
    root_note = note_to_number(root_note)
    notes = [(root_note + i)%12 for i in halftones]
    return notes

def major_scale(root_note):
    return notes_halftones_from_root(root_note, [0, 2, 4, 5, 7, 9, 11])

def minor_scale(root_note):
    return notes_halftones_from_root(root_note, [0, 2, 3, 5, 7, 8, 10])

def pentationic_major_scale(root_note):
    return notes_halftones_from_root(root_note, [0, 2, 4, 7, 9])

def pentationic_minor_scale(root_note):
    return notes_halftones_from_root(root_note, [0, 2, 3, 7, 8])
    
def major_chord(root_note):
    return notes_halftones_from_root(root_note, [0, 4, 7])
    
def minor_chord(root_note):
    return notes_halftones_from_root(root_note, [0, 3, 7])

def triad_in_major_scale(root_note_in_scale, chord_number):
    scale = major_scale(root_note_in_scale)
    note_indices = notes_halftones_from_root(chord_number-1, [0, 2, 4])
    return [scale[i%len(scale)] for i in note_indices]

def triad_in_minor_scale(root_note_in_scale, chord_number):
    scale = minor_scale(root_note_in_scale)
    note_indices = notes_halftones_from_root(chord_number-1, [0, 2, 4])
    return [scale[i%len(scale)] for i in note_indices]

def names(note_numbers):
    if isinstance(note_numbers, list):
        return '\t'.join([note_number_to_name(note) for note in note_numbers])
    else:
        return note_number_to_name(note_numbers)

def chord_to_name(note_numbers):
    for i in range(1, 13):
        if note_numbers == major_chord(i):
            return note_number_to_name(i) + ' Major'
        if note_numbers == minor_chord(i):
            return note_number_to_name(i) + ' Minor'
    return 'Could not find name of chord: ' + str(note_numbers)

print(names(pentationic_major_scale('C')))
for i in [1, 4, 6, 5]:
    print(chord_to_name(triad_in_minor_scale('C', i)))