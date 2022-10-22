# random-access-music

import vlc
import time
import random
import os
import glob

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

MUSIC_DIR = BASE_DIR / 'jo-music-lib/'
music_lib = []

for (path, dir, files) in os.walk(MUSIC_DIR):
    for f in files:
        ext = os.path.splitext(f)[-1]

        if ext == '.m4a':
            music_lib.append('%s/%s' % (path, f))


print(music_lib)

