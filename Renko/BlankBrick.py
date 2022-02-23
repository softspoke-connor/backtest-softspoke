from Renko import ceil, floor, BullBrick, BearBrick


class BlankBrick:
    def __init__(self, price):
        self.price = price
        self.bull = self._calculate_bull()
        self.bear = self._calculate_bear()

    def _calculate_bull(self):
        return (ceil(self.price * 1000) / 1000) + 0.001

    def _calculate_bear(self):
        return (floor(self.price * 1000) / 1000) - 0.001

    def __is_bull(self):
        return self.price >= self.bull

    def __is_bear(self):
        return self.price <= self.bear

    def feed(self, price):
        self.price = price

        if self.__is_bull():
            return BullBrick(price)
        elif self.__is_bear():
            return BearBrick(price)
        else:
            return self
