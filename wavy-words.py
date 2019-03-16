import sys, time, os, math, signal

def sigint(sig, frame):
    print("\nAll Done! :p")
    exit(0)

def sigwinch(sig, frame):
    wave.setup()

class SinWordWave:
    def __init__(self, input_string, period):
        self.str = input_string
        self.current_degree = 0
        self.period = period
        self.setup()

    def setup(self):
        try:
            columns = os.get_terminal_size(0).columns
        except OSError:
            columns = os.get_terminal_size(1).columns
        self.min_offset = 0
        self.max_offset = int(columns) - len(self.str)
        self.amplitude = round(self.max_offset / 2) - 1
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
    signal.signal(signal.SIGINT, sigint)
    signal.signal(signal.SIGWINCH, sigwinch)
    if len(sys.argv) < 2:
        print("You need to pass in a string for the wave at least...")
        exit(0)

    wave = SinWordWave(sys.argv[1], None)
    wave.start_the_wave()
