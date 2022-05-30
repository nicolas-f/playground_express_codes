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
        sine_wave[i] = int(math.sin(math.pi * 2 * i * (frequency / sample_rate)) * volume * (2 ** 15) + 2 ** 15)
    return RawSample(sine_wave, sample_rate=sample_rate)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = AudioOut(board.SPEAKER)

# A single sine wave sample is hundredths of a second long. If you set loop=False, it will play
# a single instance of the sample (a quick burst of sound) and then silence for the rest of the
# duration of the time.sleep(). If loop=True, it will play the single instance of the sample
# continuously for the duration of the time.sleep().

red = [255, 255, 204, 51, 0, 0, 0, 51, 204, 255]
green = [0, 153, 255, 255, 255, 255, 102, 0, 0, 0]
blue = [0, 0, 0, 0, 102, 255, 255, 255, 255, 153]
tone_time = 2
while True:
    if button.value:  # button is pushed
        time.sleep(2)
        for i in range(90, 90+16):            
            start = time.monotonic()
            freq = round(440 * 2**((i-69) / 12.0))
            print("%d Hz" % freq)
            sine_wave_sample = generate_sin(SAMPLERATE, freq, tone_volume)
            audio.play(sine_wave_sample, loop=True)  # Play the single sine_wave sample continuously...
            time.sleep(max(0, tone_time - (time.monotonic()-start)))  # for the duration of the sleep (in seconds)
            audio.stop()  # and then stop.
            time.sleep(0.1)

