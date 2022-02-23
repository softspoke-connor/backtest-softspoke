from Renko import BlankBrick, ceil


class BearBrick(BlankBrick):
    def _calculate_bull(self):
        return (ceil(self.price * 1000) / 1000) + (0.001 * 2)

    def _calculate_bear(self):
        return (ceil(self.price * 1000) / 1000) - 0.001
