from typing import Iterable


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"Deck({self.row}, {self.column}, alive={self.is_alive})"


class Ship:
    def __init__(self,
                 start: tuple[int, int],
                 end: tuple[int, int],
                 is_drowned: bool = False) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = []

        if start[0] == end[0]:
            for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                self.decks.append(Deck(start[0], i))
        elif start[1] == end[1]:
            for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                self.decks.append(Deck(i, start[1]))

    def get_deck(self, row: int, column: int) -> Deck:
        return next((deck for deck in self.decks if
                     deck.row == row and deck.column == column), None)

    def fire(self, row: int, column: int) -> str:
        if self.is_drowned:
            return "Already Sunk!"
        current_deck = self.get_deck(row, column)
        if not current_deck.is_alive:
            return "Already hit!"
        current_deck.is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True
            return "Sunk!"
        return "Hit!"

    def __repr__(self) -> str:
        return (f"Ship from ({self.start[0]}, {self.start[1]})"
                f" to ({self.end[0]}, {self.end[1]})")


class Battleship:
    def __init__(self, ships: Iterable) -> None:
        self.field = {}
        self.ships = []
        self.area_size = 10
        self.area = [["   ~   " for _ in range(self.area_size)] for _ in
                     range(self.area_size)]

        for ship_coords in ships:
            ship = Ship(ship_coords[0], ship_coords[1])
            self.ships.append(ship)
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError(
                        f"Invalid ship placement: "
                        f"overlap at ({deck.row}, {deck.column})")
                self.field[(deck.row, deck.column)] = ship

            for deck in ship.decks:
                self.area[deck.row][deck.column] = "   □   "

    def print_field(self) -> None:
        for index, ship in enumerate(self.ships):
            print(index + 1, "Ship:", ship)

    def print_area(self) -> None:
        for row in self.area:
            print(*row)

    def fire(self, location: tuple[int, int]) -> str:
        ship = self.field.get(location)
        if ship:
            return ship.fire(*location)
        return "Miss!"
