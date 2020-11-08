from RandomMusic.tones import random_note, create_note, similar_note

import math

all_effects = []

# helper function
def post_process(frames, stereo=True):
    num_frames = 500.0
    num_frames = min(num_frames, float(len(frames) // 2))
    if stereo:
        for i in range(int(num_frames)):
            frames[i] = (
                frames[i][0] * float(i) / num_frames,
                frames[i][1] * float(i) / num_frames,
            )
            frames[-i] = (
                frames[-i][0] * float(i) / num_frames,
                frames[-i][1] * float(i) / num_frames,
            )
    else:
        for i in range(int(num_frames)):
            frames[i] = frames[i] * float(i) / num_frames
            frames[-i] = frames[-i] * float(i) / num_frames
    return frames


# helper function
def notes_to_tones(notes):
    if notes:
        note1 = notes[0]
        note2 = notes[1]
    else:
        note1 = random_note()
        note2 = similar_note(note1)
    tone1 = create_note(note1, 0.5)
    tone2 = create_note(note2, 0.5)
    return tone1, tone2


# play a note left, then a note right
def left_right(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []

    segment = []
    for _ in range(length // 2):
        segment += [(next(tone1), 0)]
    frames += post_process(segment)

    segment = []
    for _ in range(length // 2):
        segment += [(0, next(tone2))]
    frames += post_process(segment)

    return post_process(frames)


all_effects += [left_right]


# play a note, then pause, then play another note, then pause
def repeat_with_pause(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []

    segment = []
    for _ in range(length // 4):
        segment += [(next(tone1), next(tone1))]
    frames += post_process(segment)

    segment = []
    for _ in range(length // 4):
        segment += [(0, 0)]
    frames += post_process(segment)

    segment = []
    for _ in range(length // 4):
        segment += [(next(tone2), next(tone2))]
    frames += post_process(segment)

    segment = []
    for _ in range(length // 4):
        segment += [(0, 0)]
    frames += post_process(segment)

    return post_process(frames)


all_effects += [repeat_with_pause]


# play a note, then fade
def faded_note(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    mute_step = 1.0 / length
    for i in range(length):
        mute = mute_step * i
        t = next(tone1) * mute
        frames += [(t, t)]

    return post_process(frames)


all_effects += [faded_note]
#
#
# # slowly swap between two tones
# def swap_notes(notes=None, length=8000):
#     tone1, tone2 = notes_to_tones(notes)
#
#     frames = []
#     mute_step = 1.0 / length
#     for i in range(length):
#         mute = mute_step * i
#         t1 = next(tone1)
#         t2 = next(tone2)
#         t = t1 * mute + t2 * (1.0 - mute)
#         frames += [(t, t)]
#
#     return post_process(frames)
#
#
# all_effects += [swap_notes]


# add a sine wave to the music
def ghostly_wave(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    mute_step = 1.0 / length * 10
    for i in range(length):
        mute = mute_step * i
        t1 = next(tone1) * math.sin(mute)
        t2 = next(tone2) * math.sin(mute)
        frames += [(t1, t2)]

    return post_process(frames)


all_effects += [ghostly_wave]


# silence
def silence(notes=None, length=8000):
    frames = [(0, 0) for _ in range(length)]
    return frames


all_effects += [silence]


# climb from 0 to tone
def climber(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    mute_step = 1.0 / length
    for i in range(length):
        t1 = next(tone1) * mute_step * i
        t2 = next(tone2) * mute_step * i
        frames += [(t1, t2)]

    return post_process(frames)


all_effects += [climber]


# climb from 0 to tone, then drop to 0
def hill(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    mute_step = 1.0 / (length / 2)

    segment = []
    for i in range(length // 2):
        t1 = next(tone1) * (0.0 + mute_step * i)
        t2 = next(tone2) * (0.0 + mute_step * i)
        segment += [(t1, t2)]
    frames += post_process(segment)

    segment = []
    for i in range(length // 2):
        t1 = next(tone1) * (1.0 - mute_step * i)
        t2 = next(tone2) * (1.0 - mute_step * i)
        segment += [(t1, t2)]
    frames += post_process(segment)

    return post_process(frames)


all_effects += [hill]
#
#
# # rapidly swap between two tones
# def swap_notes_quick(notes=None, length=8000):
#     tone1, tone2 = notes_to_tones(notes)
#
#     frames = []
#     mute_step = 1.0 / length / 10.0
#     for _ in range(10):
#         for i in range(length // 10):
#             mute = mute_step * i
#             t1 = next(tone1)
#             t2 = next(tone2)
#             t = t1 * mute + t2 * (1.0 - mute)
#             frames += [(t, t)]
#
#     return post_process(frames)
#
#
# all_effects += [swap_notes_quick]


# fall from tone to 0
def faller(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    mute_step = 1.0 / length
    for i in range(length):
        t1 = next(tone1) * (1.0 - mute_step * i)
        t2 = next(tone2) * (1.0 - mute_step * i)
        frames += [(t1, t2)]

    return post_process(frames)


all_effects += [faller]

#
# # left, right, then center
# def uppercut(notes=None, length=8000):
#     tone1, tone2 = notes_to_tones(notes)
#
#     frames = []
#
#     segment = []
#     for i in range(length // 4):
#         t1 = next(tone1)
#         t2 = 0
#         segment += [(t1, t2)]
#     frames += post_process(segment)
#
#     segment = []
#     for i in range(length // 4):
#         t1 = 0
#         t2 = next(tone2)
#         segment += [(t1, t2)]
#     frames += post_process(segment)
#
#     segment = []
#     for i in range(length // 6):
#         t1 = next(tone1)
#         t2 = next(tone1)
#         segment += [(t1, t2)]
#     frames += post_process(segment)
#
#     segment = []
#     for i in range(length // 6):
#         t1 = next(tone2)
#         t2 = next(tone2)
#         segment += [(t1, t2)]
#     frames += post_process(segment)
#
#     segment = []
#     for i in range(length // 6):
#         t1 = next(tone1)
#         t2 = next(tone2)
#         segment += [(t1, t2)]
#     frames += post_process(segment)
#
#     return post_process(frames)
#
#
# all_effects += [uppercut]


# just play a note
def basic_note(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    for i in range(length):
        t1 = next(tone1)
        t2 = next(tone2)
        frames += [(t1, t2)]

    return post_process(frames)


all_effects += [basic_note]


# just play half a note
def half_note(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    for i in range(length // 2):
        t1 = next(tone1)
        t2 = next(tone2)
        frames += [(t1, t2)]
    frames = post_process(frames)
    for i in range(length // 2):
        t1 = 0.0
        t2 = 0.0
        frames += [(t1, t2)]

    return post_process(frames)


all_effects += [half_note]


# just play a quarter note
def quarter_note(notes=None, length=8000):
    tone1, tone2 = notes_to_tones(notes)

    frames = []
    for i in range(length // 4):
        t1 = next(tone1)
        t2 = next(tone2)
        frames += [(t1, t2)]
    frames = post_process(frames)
    for i in range(length - length // 4):
        t1 = 0.0
        t2 = 0.0
        frames += [(t1, t2)]

    return post_process(frames)


all_effects += [quarter_note]
