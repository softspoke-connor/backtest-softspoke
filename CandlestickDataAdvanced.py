from v20.instrument import Candlestick, CandlestickData


class CandlestickAdvanced(Candlestick):
    def __init__(self, granularity, **kwargs):
        super().__init__(**kwargs)
        self.granularity = granularity
        self.mid = CandlestickData()

        self.first_feed = False
        self.completion_time = None

    def feed(self, candlestick: Candlestick):
        if not self.first_feed:
            self.time = self.__round_time(candlestick.time, round_type=False)
            self.mid.o = candlestick.mid
            self.mid.h = candlestick.mid
            self.mid.l = candlestick.mid
            self.mid.c = candlestick.mid
            self.completion_time = self.__add_time()
            self.first_feed = True
        else:
            if self.__is_complete():
                self.complete = True

        if candlestick.mid > self.mid.h:
            self.mid.h = candlestick.mid
        elif candlestick.mid < self.mid.l:
            self.mid.l = candlestick.mid

        self.mid.c = candlestick.mid

    def __round_time(self, time, round_type=None):
        return  # TODO

    def __add_time(self):
        return  # TODO

    def __is_complete(self):
        return  # TODO
