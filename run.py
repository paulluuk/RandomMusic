from RandomMusic.music import create_song


def run():
    s = create_song()
    s.save()

if __name__ == "__main__":
    run()
