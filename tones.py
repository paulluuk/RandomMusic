import math
import random

BYTES = 2
MAX_DEPTH = max_amplitude = float(int((2 ** (BYTES * 8)) / 2) - 1)
CD_QUALITY_FRAMERATE = 44100


def sine_wave(frequency=440.0, framerate=CD_QUALITY_FRAMERATE, amplitude=0.5):
    if amplitude > 1.0:
        amplitude = 1.0
    if amplitude < 0.0:
        amplitude = 0.0
    i = 0.0
    while True:
        i += 1.0
        yield MAX_DEPTH * float(amplitude) * math.sin(
            2.0 * math.pi * float(frequency) * (float(i) / float(framerate))
        )


def create_note(note, volume):
    return sine_wave(
        frequency=notes[note], framerate=CD_QUALITY_FRAMERATE, amplitude=volume
    )


def random_note():
    global notes
    return random.choice([note for note in notes.keys() if note[1] in "34"])


def similar_note(note):
    global notes
    options = [lower_note(note), higher_note(note)]
    return random.choice(options)


def lower_note(note):
    global notes
    alpha = "ABCDEFG"
    num = "12345678"
    if note[1] in num[1:]:
        new_note = note[0] + num[num.index(note[1]) - 1]
    elif note[0] in alpha[1:]:
        new_note = alpha[alpha.index(note[0]) - 1] + note[1]
    else:
        new_note = note

    if new_note in notes:
        return new_note
    else:
        return note


def higher_note(note):
    global notes
    alpha = "ABCDEFG"
    num = "12345678"
    if note[1] in num[:-1]:
        new_note = note[0] + num[num.index(note[1]) + 1]
    elif note[0] in alpha[:-1]:
        new_note = alpha[alpha.index(note[0]) + 1] + note[1]
    else:
        new_note = note

    if new_note in notes:
        return new_note
    else:
        return note


# I commented the tones that I thought were not great for music
# uncommenting them will add more variation in notes, but mostly
# very low and very high pitch noise.

notes = {}
# notes["A1"] = 28
# notes["B1"] = 31
# notes["C1"] = 33
# notes["D1"] = 37
# notes["E1"] = 41
# notes["F1"] = 44
# notes["G1"] = 49
notes["A2"] = 55
notes["B2"] = 62
notes["C2"] = 65
notes["D2"] = 73
notes["E2"] = 82
notes["F2"] = 87
notes["G2"] = 98
notes["A3"] = 110
notes["B3"] = 123
notes["C3"] = 131
notes["D3"] = 147
notes["E3"] = 165
notes["F3"] = 175
notes["G3"] = 196
notes["A4"] = 220
notes["B4"] = 247
notes["C4"] = 262
notes["D4"] = 294
notes["E4"] = 330
notes["F4"] = 349
notes["G4"] = 392
notes["A5"] = 440
notes["B5"] = 494
notes["C5"] = 523
notes["D5"] = 587
notes["E5"] = 659
notes["F5"] = 698
notes["G5"] = 784
notes["A6"] = 880
notes["B6"] = 988
notes["C6"] = 1047
notes["D6"] = 1175
notes["E6"] = 1319
notes["F6"] = 1397
notes["G6"] = 1568
# notes["A7"] = 1760
# notes["B7"] = 1976
# notes["C7"] = 2093
# notes["D7"] = 2349
# notes["E7"] = 2637
# notes["F7"] = 2794
# notes["G7"] = 3136
# notes["A8"] = 3520
# notes["B8"] = 3951
# notes["C8"] = 4186
# notes["D8"] = 4699
# notes["E8"] = 5274
# notes["F8"] = 5588
# notes["G8"] = 6272
