import sys, time
import os
import math

class SinWordWave:
    def __init__(self, input_string, period):
        rows, columns = os.popen('stty size', 'r').read().split()
        self.str = input_string
        self.min_offset = 0
        self.max_offset = int(columns)-len(self.str)
        self.amplitude = round(self.max_offset / 2) - 1
        self.period = period
        self.current_degree = 0
        self.offset = self.calculate_offset()

    def calculate_offset(self):
        offset = round(self.amplitude * math.sin(10 * math.radians(self.current_degree))) + self.amplitude
        self.current_degree = self.current_degree + 1 if self.current_degree < 360 else 0
        return offset

    def start_the_wave(self):
        while True:
            time.sleep(0.1)
            print(' ' * self.offset + self.str, flush=True)
            self.offset = self.calculate_offset()


if __name__ == "__main__":
    try:
        wave = SinWordWave(sys.argv[1], None)
    except IndexError:
        print("You need to pass in a string for the wave at least...")

    wave.start_the_wave()
