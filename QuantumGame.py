from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer


def quantum_choice():
    """Returns 0 or 1 with equal probability using a quantum coin flip."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    simulator = Aer.get_backend('aer_simulator')
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1).result()
    counts = result.get_counts()

    return int(list(counts.keys())[0])


class QuantumTicTacToe:
    def __init__(self):
        self.board = {(i, j): [] for i in range(3) for j in range(3)}
        self.moves = []
        self.turn = "X"
        self.move_number = 1
        self.collapsed = False

    def is_valid_move(self, p1, p2):
        if p1 == p2:
            print("  Error: Both positions must be different.")
            return False
        for p in (p1, p2):
            if not (0 <= p[0] <= 2 and 0 <= p[1] <= 2):
                print(f"  Error: Position {p} is out of range (use 0-2).")
                return False
        return True

    def place_move(self, p1, p2):
        if not self.is_valid_move(p1, p2):
            return False
        label = f"{self.turn}{self.move_number}"
        self.board[p1].append(label)
        self.board[p2].append(label)
        self.moves.append((label, p1, p2))
        self.move_number += 1
        self.turn = "O" if self.turn == "X" else "X"
        return True

    def collapse(self):
        self.collapsed = True
        chosen_positions = {}

        for label, p1, p2 in self.moves:
            bit = quantum_choice()
            chosen = p1 if bit == 0 else p2
            other  = p2 if chosen == p1 else p1
            chosen_positions[label] = chosen

            if label in self.board[other]:
                self.board[other].remove(label)

        for pos in self.board:
            surviving = [lbl for lbl in self.board[pos]
                         if chosen_positions.get(lbl) == pos]
            if len(surviving) > 1:
                surviving.sort(key=lambda l: int(l[1:]))
                self.board[pos] = [surviving[-1]]
            elif len(surviving) == 1:
                self.board[pos] = [surviving[0]]
            else:
                self.board[pos] = []

    def check_winner(self):
        lines = [
            [(0,0),(0,1),(0,2)],
            [(1,0),(1,1),(1,2)],
            [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)],
            [(0,1),(1,1),(2,1)],
            [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)],
            [(0,2),(1,1),(2,0)]
        ]
        for line in lines:
            values = []
            for pos in line:
                cell = self.board[pos]
                if len(cell) == 1:
                    values.append(cell[0][0])
            if len(values) == 3 and len(set(values)) == 1:
                return values[0]
        return None

    def is_draw(self):
        all_filled = all(len(self.board[pos]) == 1 for pos in self.board)
        return all_filled and self.check_winner() is None

    def print_board(self):
        print("-" * 25)
        for i in range(3):
            row = ""
            for j in range(3):
                cell = self.board[(i, j)]
                row += (",".join(cell) if cell else ".").ljust(7)
            print(row)
        print("-" * 25)


def parse_position(prompt):
    """Safely parse 'row col' input and return a (row, col) tuple."""
    while True:
        try:
            parts = input(prompt).split()
            if len(parts) != 2:
                raise ValueError
            r, c = int(parts[0]), int(parts[1])
            if not (0 <= r <= 2 and 0 <= c <= 2):
                print("  Values must be 0, 1, or 2. Try again.")
                continue
            return (r, c)
        except ValueError:
            print("  Invalid input. Enter two numbers separated by a space, e.g. '1 2'.")


def main():
    print("=== Quantum Tic-Tac-Toe ===")
    print("Each turn: enter TWO different cells for your quantum move.")
    print("Positions are (row col) with values 0-2.")
    print("Example: '0 1' means row 0, column 1\n")

    game = QuantumTicTacToe()
    quantum_rounds = 4

    for _ in range(quantum_rounds):
        game.print_board()
        print(f"{game.turn}'s quantum move (move #{game.move_number})")

        while True:
            p1 = parse_position("  First  position (row col): ")
            p2 = parse_position("  Second position (row col): ")
            if game.place_move(p1, p2):
                break

    print("\n⚛️  Collapsing quantum states...")
    game.collapse()

    print("\nBoard after collapse:")
    game.print_board()

    winner = game.check_winner()
    if winner:
        print(f"\n🏆 Winner: {winner}!")
    elif game.is_draw():
        print("\n🤝 It's a draw!")
    else:
        print("\nNo winner — some cells are still empty after collapse.")


if __name__ == "__main__":
    main()
