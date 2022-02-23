from Renko import BlankBrick, floor


class BullBrick(BlankBrick):
    def _calculate_bull(self):
        return (floor(self.price * 1000) / 1000) + 0.001

    def _calculate_bear(self):
        return (floor(self.price * 1000) / 1000) - (0.001 * 2)
