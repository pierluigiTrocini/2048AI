import numpy as np

N = 4

def make_move(self, move: str, grid: np.array) -> np.array:
    for i in range(N):
        if move in "lr":
            this = grid[i, :]
        else:
            this = grid[:, i]

        flipped = False
        if move in "rd":
            flipped = True
            this = this[::-1]

        this_n = self._get_nums(this)

        new_this = np.zeros_like(this)
        new_this[: len(this_n)] = this_n

        if flipped:
            new_this = new_this[::-1]

        if move in "lr":
            grid[i, :] = new_this
        else:
            grid[:, i] = new_this
    
    return grid