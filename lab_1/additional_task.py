import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

notes = [
    "A4", "C5", "D5", "D5", "D5", "E5", "F5", "F5",
    "F5", "G5", "E5", "E5", "D5", "C5", "C5", "D5",

    "A4", "C5", "D5", "D5", "D5", "E5", "F5", "F5",
    "F5", "G5", "E5", "E5", "D5", "C5", "C5", "D5",

    "A4", "C5", "D5", "D5", "D5", "F5", "G5", "G5",
    "G5", "A5", "Bb5", "Bb5", "A5", "G5", "A5", "D6"
]

fs = 5000
note_length = 0.3
semitones = {
    "C": 0, "D": 2, "E": 4, "F": 5,
    "G": 7, "A": 9, "Bb": 10, "B": 11
}

audio = []



for note in notes:
    name, octave = note[:-1], int(note[-1])
    midi = 12 * (octave + 1) + semitones[name]
    frequency = 440 * 2 ** ((midi - 69) / 12)

    t = np.arange(int(note_length * fs)) / fs
    envelope = np.minimum(1, t / 0.01) * np.minimum(
        1, (note_length - t) / 0.04
    )
    audio.extend(envelope * np.sin(2 * np.pi * frequency * t))

audio_array = np.array(audio)
time_axis = np.arange(len(audio_array)) / fs

plt.figure(figsize=(12, 4))
plt.plot(time_axis, audio_array)
plt.grid(True)
plt.show()

sd.play(np.array(audio), fs)
sd.wait()