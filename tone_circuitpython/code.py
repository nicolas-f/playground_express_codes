# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import array
import math
import board
import digitalio

try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!
tone_volume = 0.2  # Increase this to increase the volume of the tone.
FREQUENCY = 1720  # Hz
SAMPLERATE = 48000  # 8000 samples/second, recommended!

button = digitalio.DigitalInOut(board.BUTTON_A)
button.switch_to_input(pull=digitalio.Pull.DOWN)

def generate_sin(sample_rate, frequency, volume):
    # Generate one period of sine wav.
    length = sample_rate // frequency
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * volume * (2 ** 15) + 2 ** 15)
    return RawSample(sine_wave, sample_rate=sample_rate)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = AudioOut(board.SPEAKER)
sine_wave_sample = generate_sin(SAMPLERATE, FREQUENCY, tone_volume)

# A single sine wave sample is hundredths of a second long. If you set loop=False, it will play
# a single instance of the sample (a quick burst of sound) and then silence for the rest of the
# duration of the time.sleep(). If loop=True, it will play the single instance of the sample
# continuously for the duration of the time.sleep().

while True:
    if button.value:  #and then stop.
