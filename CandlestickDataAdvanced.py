from v20.instrument import Candlestick, CandlestickData
from datetime import datetime, timedelta


class CandlestickAdvanced(Candlestick):
    def __init__(self, granularity, **kwargs):
        super().__init__(**kwargs)
        self.granularity = granularity
        self.mid = CandlestickData()

        self.first_feed = False
        self.completion_time = None

    def feed(self, candlestick: Candlestick):
        if not self.first_feed:
            self.time = self.__round_time(candlestick.time, round_type=False) + "000Z"
            self.mid.o = candlestick.mid.c
            self.mid.h = candlestick.mid.c
            self.mid.l = candlestick.mid.c
            self.mid.c = candlestick.mid.c
            self.completion_time = self.__add_time()
            self.first_feed = True
        else:
            if self.__is_complete(candlestick.time):
                self.complete = True

        if candlestick.mid.c > self.mid.h:
            self.mid.h = candlestick.mid.c
        elif candlestick.mid.c < self.mid.l:
            self.mid.l = candlestick.mid.c

        self.mid.c = candlestick.mid.c

    def __round_time(self, time, round_type=None):
        dt = datetime.strptime(time[:-4], "%Y-%m-%dT%H:%M:%S.%f")

        if self.granularity == "M15":
            if dt.minute >= 45:
                minute = 45
            elif dt.minute >= 30:
                minute = 30
            elif dt.minute >= 15:
                minute = 15
            else:
                minute = 0

            dt = dt.replace(minute=minute, second=0, microsecond=0)
            return datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            raise NotImplementedError("This granularity is either invalid or has not yet been implemented.")

    def __add_time(self):
        if self.granularity == "M15":
            return datetime.strptime(self.time[:-4], "%Y-%m-%dT%H:%M:%S.%f") + timedelta(minutes=15)
        else:
            raise NotImplementedError("This granularity is either invalid or has not yet been implemented.")

    def __is_complete(self, time):
        return time > datetime.strftime(self.completion_time, "%Y-%m-%dT%H:%M:%S.%f")
