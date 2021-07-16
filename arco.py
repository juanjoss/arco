from collections import Counter
from bitstream import BitStream
import time

class ArithmeticCoding():
    def __init__(self, debug=False, PRECISION=32):
        # constants
        self.__PRECISION = PRECISION
        self.__FULL = 2**self.__PRECISION
        self.__HALF = self.__FULL // 2
        self.__QUARTER = self.__HALF // 2
        
        # encoder/decoder attributes
        self.__low = 0
        self.__high = (1 << self.__PRECISION) - 1
        self.__freq_table = None
        self.__data_len = 0
        self.__code = BitStream()
        self.__trails = 0
        
        # debug
        self.debug = debug
        self.elapsed = None

    def __build_frequency_table(self, data):
        """
            Non optimal model, the decoder will need the frequency table.
        """
        freq_table = Counter(data).items()
        self.__data_len = len(data)
        return dict(freq_table)

    def __cum_freq(self, symbol):
        freq = 0

        for c in self.__freq_table:
            freq += self.__freq_table[c]

            if c == symbol:
                break

        return freq

    def encode(self, data):
        self.elapsed = time.time()
        self.__freq_table = self.__build_frequency_table(data) # non optimal model

        # iterate over every symbol in data
        for c in data:
            # compute current range
            r = (self.__high - self.__low) + 1
                
            # update high and low
            fc = self.__freq_table[c]

            N = self.__cum_freq(c)
            C = N - fc
            T = self.__data_len

            self.__high = self.__low + ((r*N) // T)
            self.__low = self.__low + ((r*C) // T)

            while True:
                if self.__high < self.__HALF:
                    self.__code.write(0, bool)
                    self.__code.write([1]*self.__trails, bool)
                    self.__trails = 0

                    # scale lower half
                    self.__low *= 2
                    self.__high *= 2
                elif self.__low >= self.__HALF:
                    self.__code.write(1, bool)
                    self.__code.write([0]*self.__trails, bool)

                    # scale upper half
                    self.__low = 2 * (self.__low - self.__HALF)
                    self.__high = 2 * (self.__high - self.__HALF)
                elif self.__low >= self.__QUARTER and self.__high < 3*self.__QUARTER:
                    self.__trails += 1
                    self.__low = 2 * (self.__low - self.__QUARTER)
                    self.__high = 2 * (self.__high - self.__QUARTER)
                else:
                    break


        # add last bits
        self.__trails += 1

        if self.__low <= self.__QUARTER:
            self.__code.write(0, bool)
            self.__code.write([1]*self.__trails, bool)
        else:
            self.__code.write(1, bool)
            self.__code.write([0]*self.__trails, bool)

        # debug log if enabled
        if self.debug:
            print("code: {}\n".format(self.__code))
            print("code length: {}\n".format(len(self.__code)))
            print("data encoded in: {} seconds".format((time.time() - self.elapsed)))

        return self.__code

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        data = open(filename).read()

        e = ArithmeticCoding(debug=True)
        code = e.encode(data)
    else:
        print("\nusage: python3 arco.py <filename>\n")
        sys.exit()
