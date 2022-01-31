from math import ceil, floor


class Renko:
    def __init__(self, brick_size=0.001):
        self.brick_size = brick_size
        self.signal, self.previous_signal = None, None
        self.bull_signal, self.bear_signal = None, None
        self.execution_ready = False

    def __calculate_bull(self, close_data):
        return round(ceil(close_data / self.brick_size) * self.brick_size, 3)

    def __calculate_bear(self, close_data):
        return round(floor(close_data / self.brick_size) * self.brick_size, 3)

    def feed(self, close_data):
        if self.bull_signal is None:
            self.bull_signal = self.__calculate_bull(close_data) + self.brick_size
            self.bear_signal = self.__calculate_bear(close_data) - self.brick_size
        elif close_data >= self.bull_signal:
            self.previous_signal = self.signal
            self.signal = True
            self.execution_ready = self.previous_signal != self.signal
            self.bull_signal = self.__calculate_bull(close_data)
            self.bear_signal = self.__calculate_bear(close_data) - (self.brick_size * 2)
        elif close_data <= self.bear_signal:
            self.previous_signal = self.signal
            self.signal = False
            self.execution_ready = self.previous_signal != self.signal
            self.bull_signal = self.__calculate_bull(close_data) + (self.brick_size * 2)
            self.bear_signal = self.__calculate_bear(close_data)
        else:
            self.execution_ready = False

    def is_bull(self):
        bullish = self.signal is True and self.execution_ready
        return bullish

    def is_bear(self):
        bearish = self.signal is False and self.execution_ready
        return bearish
