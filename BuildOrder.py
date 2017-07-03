import cybw


def get_build_order_from_file():
    raise NotADirectoryError


class BuildOrder:
    def __init__(self):
        self.build_order = []

    def add(self, unit):
        self.build_order.append(unit)
