import random
import struct
import os

from tones import CD_QUALITY_FRAMERATE

import wave
from pydub import AudioSegment

adjectives = []
nouns = []


def random_title():
    global adjectives, nouns
    if len(adjectives) == 0:
        with open("adjectives.txt", "r") as f:
            adjectives = f.readlines()
            adjectives = [a.strip("\n") for a in adjectives]
    if len(nouns) == 0:
        with open("nouns.txt", "r") as f:
            nouns = f.readlines()
            nouns = [a.strip("\n") for a in nouns]

    return random.choice(adjectives).title() + " " + random.choice(nouns).title()


def create_wav(music, n_channels=2, bytes=2, framerate=CD_QUALITY_FRAMERATE):
    title = random_title()
    author = "pluk's random music generator"
    filename = title.replace(" ", "_") + ".wav"
    pathname = os.path.join("generated", filename)
    os.makedirs("generated", exist_ok=True)

    w = wave.open(pathname, "w")
    w.setparams((n_channels, bytes, framerate, len(music), "NONE", "not compressed"))

    frames = []

    for (tone1, tone2) in music:
        try:
            frames += [struct.pack("h", int(tone1))]
            frames += [struct.pack("h", int(tone2))]
        except Exception as e:
            print(tone1, tone2)
            raise e

    w.writeframesraw(b"".join(frames))

    AudioSegment.from_wav(pathname).export(
        pathname.replace(".wav", ".mp3"),
        format="mp3",
        tags={"title": title, "artist": author},
    )
