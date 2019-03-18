import sys, time, os, math, signal, argparse

def sigint(sig, frame):
    print("\nAll Done! :p")
    exit(0)

def sigwinch(sig, frame):
    wave.setup()

class SinWordWave:
    def __init__(self, input_string=None, freq=10, in_file=None):
        if input_string and in_file:
            raise AttributeError("Cannot define both an input string and an input file.")	

        self.columns = None
        self._update_columns()
        self.words = None

        if input_string:
            self.current_str = input_string
            self.max_offset = int(self.columns) - len(self.current_str)
            
        if in_file:
            self.words = self._get_words(in_file)
            self.num_words = len(self.words)
            self.current_str_idx = 0
            self.current_str = self.words[self.current_str_idx]
            self.max_offset = self._calculate_max_offset()
            
        self.current_degree = 0
        self.freq = freq
        self.setup()

    def _get_words(self, in_file):
    	return [word for line in open(in_file, 'r') for word in line.split()]

    def _calculate_max_offset(self):
        greatest_str_len = 0
        for word in self.words:
            greatest_str_len = len(word) if len(word) > greatest_str_len else greatest_str_len
        return int(self.columns) - greatest_str_len

    def _update_columns(self):
        try:
            self.columns = os.get_terminal_size(0).columns
        except OSError:
            self.columns = os.get_terminal_size(1).columns

    def _update_current_string(self):
        if not self.words:
            return
        if self.current_str_idx < self.num_words - 1:
            self.current_str_idx = self.current_str_idx + 1
        else:
            self.current_str_idx = 0
        self.current_str = self.words[self.current_str_idx]


    def setup(self):
        self._update_columns()
        self.amplitude = round(self.max_offset / 2) - 1
        self.offset = self.calculate_offset()

    def calculate_offset(self):
        offset = round(self.amplitude * math.sin(self.freq * math.radians(self.current_degree))) + self.amplitude
        self.current_degree = self.current_degree + 1 if self.current_degree < 360 else 1
        return offset

    def start_the_wave(self):
        while True:
            time.sleep(0.1)
            print(' ' * self.offset + self.current_str, flush=True)
            self._update_current_string()
            self.offset = self.calculate_offset()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint)
    signal.signal(signal.SIGWINCH, sigwinch)

    parser = argparse.ArgumentParser()
    parser.add_argument("--string", help="A string input that will be printed on each line.")
    parser.add_argument("--file", help="A file input which will be parsed out into words.")
    args = parser.parse_args()

    wave = SinWordWave(input_string=args.string, in_file=args.file)
    wave.start_the_wave()
