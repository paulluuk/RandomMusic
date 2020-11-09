import random

from create_wav import create_wav
from effects import all_effects, post_process
from tones import random_note, similar_note, create_note


class Music:
    def __init__(self, frames=None, stereo=False, notes=None):
        self.frames = [] if not frames else frames
        self.stereo = stereo
        base_note = random_note()
        if notes == None:
            self.notes = [
                base_note,
                similar_note(base_note),
                similar_note(base_note),
                similar_note(base_note),
            ]
        else:
            self.notes = notes

    def mono_to_stereo(self):
        if not self.stereo:
            self.frames = [(f, f) for f in self.frames]
            self.stereo = True

    def blur(self, num_frames=500):
        num_frames = float(min(num_frames, int(len(self.frames) // 2)))

        if self.stereo:
            for i in range(int(num_frames)):
                self.frames[i] = (
                    self.frames[i][0] * float(i) / num_frames,
                    self.frames[i][1] * float(i) / num_frames,
                )
                self.frames[-i] = (
                    self.frames[-i][0] * float(i) / num_frames,
                    self.frames[-i][1] * float(i) / num_frames,
                )
        else:
            for i in range(int(num_frames)):
                self.frames[i] = self.frames[i] * float(i) / num_frames
                self.frames[-i] = self.frames[-i] * float(i) / num_frames

    def merge(self, other):
        max_frames = min(len(other.frames), len(self.frames))

        new_frames = []
        if other.stereo:
            if not self.stereo:
                self.mono_to_stereo()
            for (l1, r1), (l2, r2) in zip(
                post_process(self.frames, stereo=self.stereo),
                post_process(other.frames[:max_frames], stereo=other.stereo),
            ):
                new_frames += [((l1 + l2) * 0.5, (r1 + r2) * 0.5)]
            stereo = True
        elif self.stereo:
            for (l1, r1), t in zip(
                post_process(self.frames, stereo=self.stereo),
                post_process(other.frames[:max_frames], stereo=other.stereo),
            ):
                new_frames += [((l1 + t) * 0.5, (r1 + t) * 0.5)]
            stereo = True
        else:
            for t1, t2 in zip(
                post_process(self.frames, stereo=self.stereo),
                post_process(other.frames[:max_frames], stereo=other.stereo),
            ):
                new_frames += [(t1 + t2) * 0.5]
            stereo = False

        return Music(new_frames, stereo, notes=self.notes)

    def __add__(self, other):
        if isinstance(other, Music):
            new_frames = []
            if self.stereo and not other.stereo:
                new_frames += self.frames
                new_frames += [(y, y) for y in other.frames]
                stereo = True
            elif not self.stereo and other.stereo:
                new_frames += [(y, y) for y in self.frames]
                new_frames += other.frames
                stereo = True
            else:
                new_frames += self.frames
                new_frames += other.frames
                stereo = self.stereo
            new = Music(new_frames, stereo, notes=self.notes)
            new.blur(200)
            return new
        else:
            raise NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Music):
            if self.stereo == other.stereo:
                self.frames += other.frames
            elif self.stereo:
                self.frames += [(y, y) for y in other.frames]
            else:
                self.mono_to_stereo()
                self.frames += other.frames
            self.blur(200)
            return self
        else:
            raise NotImplemented

    def add_effect(self, effect, length):
        frames = effect(self.notes, length)
        effect_music = Music(frames, True, notes=self.notes)
        effect_music.blur(200)
        self.__iadd__(effect_music)

    def save(self):
        self.mono_to_stereo()
        create_wav(self.frames)

    def add_beat(self, beat_length):
        beat = create_note(random.choice(["A3", "B3", "C3"]), 0.5)

        silence = [0.0 for _ in range(beat_length)]
        beat_frames = (
            post_process([next(beat) for _ in range(beat_length)], stereo=False)
            + silence
        )
        new_frames = []
        while len(new_frames) < len(self.frames):
            new_frames += beat_frames
        beat_music = Music(new_frames, False, notes=self.notes)
        beat_music.blur(200)
        return self.merge(beat_music)


def reduce(music_list):
    if len(music_list) == 1:
        return music_list[0]

    base = music_list[0]
    for other in music_list[1:]:
        base = base.merge(other)
    return base


def create_song():
    speeds = [12000, 16000, 20000, 24000, 28000, 32000]
    s = random.choice(speeds)

    print("Generating song..")

    print("Creating verse..")
    verses = []
    for _ in range(random.randint(1, 8)):
        verse = Music()
        for _ in range(random.randint(8, 20)):
            verse.add_effect(random.choice(all_effects), s)
        verses += [verse]
    verse = reduce(verses)
    if random.random() > 0.5:
        verse = verse.add_beat(s // 2)
    notes = verse.notes

    print("Creating chorus..")
    chori = []
    for _ in range(random.randint(1, 8)):
        chorus = Music(notes=notes)
        for _ in range(random.randint(8, 20)):
            chorus.add_effect(random.choice(all_effects), s)
        chori += [chorus]
    chorus = reduce(chori)
    if random.random() > 0.5:
        chorus = chorus.add_beat(s // 2)

    print("Creating bridge..")
    bridges = []
    for _ in range(random.randint(1, 8)):
        bridge = Music(notes=notes)
        for _ in range(random.randint(8, 20)):
            bridge.add_effect(random.choice(all_effects), s)
        bridges += [bridge]
    bridge = reduce(bridges)
    if random.random() > 0.5:
        bridge = bridge.add_beat(s // 2)

    print("Joining verse, chorus and bridge..")
    part1 = verse + chorus + verse + chorus + verse
    if random.random() > 0.8:
        part1 = part1.add_beat(s // 2)
    part2 = chorus + chorus
    if random.random() > 0.8:
        part2 = part2.add_beat(s // 2)
    part2 += chorus
    song = bridge + part1 + bridge + part2

    print("Completed new song!")
    return song
