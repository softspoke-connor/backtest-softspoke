from math import ceil, floor


class BlankBrick:
    def __init__(self, price):
        self.price = price
        self.bull = self._calculate_bull()
        self.bear = self._calculate_bear()

    def _calculate_bull(self):
        return round((ceil(self.price * 1000) / 1000) + 0.001, 3)

    def _calculate_bear(self):
        return round((floor(self.price * 1000) / 1000) - 0.001, 3)

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


class BearBrick(BlankBrick):
    def _calculate_bull(self):
        return round((ceil(self.price * 1000) / 1000) + (0.001 * 2), 3)

    def _calculate_bear(self):
        return round((ceil(self.price * 1000) / 1000) - 0.001, 3)


class BullBrick(BlankBrick):
    def __init__(self, price):
        super().__init__(price)

    def _calculate_bull(self):
        return round((floor(self.price * 1000) / 1000) + 0.001, 3)

    def _calculate_bear(self):
        return round((floor(self.price * 1000) / 1000) - (0.001 * 2), 3)