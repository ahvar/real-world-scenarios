# Connect Four LLD

## Problem Description

Design the backend logic for a two-player Connect Four game.

Two players alternate turns dropping discs into a board with 7 columns and 6 rows. A move is made by choosing a column. The disc falls to the lowest available row in that column. The game ends when either:

- one player connects four of their own discs horizontally, vertically, or diagonally
- the board becomes full with no winner, which is a draw

Invalid moves must be rejected without corrupting game state. Examples include:

- placing a disc into a full column
- playing out of turn
- making a move after the game has already ended

This problem is a good first LLD exercise because it forces you to separate responsibilities clearly:

- `Game` should orchestrate turns and game state
- `Board` should own grid state and placement logic
- `Player` should remain simple data

## What You Need To Build

At a minimum, your design should support:

- creating a game with two players
- making moves by column
- checking whether a move wins the game
- detecting a draw
- rejecting invalid actions cleanly
- exposing enough state for tests or a UI layer to inspect the board and outcome

## Core Entities

### Player

Represents one participant.

Recommended fields:

- `name`
- `color`

This class should stay intentionally small. It does not need game logic.

### Board

Represents the 7x6 grid and the physical rules of the board.

Recommended responsibilities:

- store the grid
- tell whether a disc can be placed in a column
- place a disc in the lowest available row
- check whether a newly placed disc created a win
- report whether the board is full
- expose cell values for tests or rendering

### Game

Represents one running game and acts as the main entry point.

Recommended responsibilities:

- store the two players
- track whose turn it is
- track the game state: in progress, won, or draw
- validate moves before mutating state
- delegate board operations to `Board`
- switch turns after a successful move
- record the winner when the game ends

## Suggested Enums

Two enums keep the state explicit and easy to reason about.

- `DiscColor`: `RED`, `YELLOW`
- `GameState`: `IN_PROGRESS`, `WON`, `DRAW`

Enums are a better choice than boolean flags because they avoid invalid combinations like "won and draw at the same time".

## Recommended Public API

### Board

```python
class Board:
    def __init__(self, rows: int = 6, cols: int = 7):
        ...

    def get_rows(self) -> int:
        ...

    def get_cols(self) -> int:
        ...

    def can_place(self, column: int) -> bool:
        ...

    def place_disc(self, column: int, color: DiscColor) -> int:
        ...

    def check_win(self, row: int, column: int, color: DiscColor) -> bool:
        ...

    def is_full(self) -> bool:
        ...

    def get_cell(self, row: int, column: int) -> Optional[DiscColor]:
        ...
```

### Game

```python
class Game:
    def __init__(self, player1, player2):
        ...

    def make_move(self, player, column: int) -> bool:
        ...

    def get_current_player(self):
        ...

    def get_game_state(self) -> GameState:
        ...

    def get_winner(self):
        ...

    def get_board(self) -> Board:
        ...
```

## How The Pieces Fit Together

The cleanest control flow is:

1. External code asks `Game` to make a move.
2. `Game` validates that the move is allowed from a turn and lifecycle perspective.
3. `Game` calls `Board.place_disc()`.
4. `Board` handles grid validation and placement.
5. `Game` asks `Board.check_win()` and `Board.is_full()`.
6. `Game` updates the winner or draw state if needed.
7. If the game continues, `Game` switches the current player.

This keeps orchestration in one place and board math in one place.

## Implementation Guide

Build this in layers. Do not start with win detection first.

### Step 1: Create the enums

Start with the smallest stable pieces.

- add `DiscColor`
- add `GameState`

This gives the rest of the code explicit state types to use.

### Step 2: Implement `Player`

Keep this class simple.

- store `name`
- store `color`

That is enough for this problem.

### Step 3: Implement the `Board` constructor and grid

Initialize a 6x7 grid of empty cells.

Recommended representation:

```python
self.grid = [[None for _ in range(cols)] for _ in range(rows)]
```

Why this matters:

- it is easy to test
- it makes placement logic straightforward
- it works naturally with directional win checks later

### Step 4: Add basic board helpers

Implement these next because other methods depend on them:

- `get_rows()`
- `get_cols()`
- `_in_bounds(row, column)`
- `get_cell(row, column)`
- `can_place(column)`

`can_place(column)` should return `False` when:

- the column index is out of range
- the top row in that column is already occupied

### Step 5: Implement `place_disc()`

This is your first core method.

Behavior:

- reject invalid columns
- reject full columns
- scan from the bottom row upward
- place the disc in the first empty cell
- return the row index where the disc landed
- return `-1` if the move could not be made

The important design choice here is that `Board` owns board-specific validation. `Game` should not be responsible for column bounds or finding where a disc lands.

### Step 6: Implement `is_full()`

This should return `True` only when no additional discs can be placed.

Simple approach:

- inspect the top row of every column
- if every top cell is occupied, the board is full

### Step 7: Implement directional win detection

This is the trickiest part, so keep it systematic.

Use four base directions:

- horizontal: `(0, 1)`
- vertical: `(1, 0)`
- diagonal down-right: `(1, 1)`
- diagonal up-right: `(-1, 1)`

For each direction:

1. start the count at `1` for the newly placed disc
2. count matching discs in the positive direction
3. count matching discs in the negative direction
4. if the total reaches `4`, it is a win

This is better than writing separate horizontal, vertical, and diagonal methods because the pattern is the same in all four cases.

### Step 8: Add `_count_in_direction()`

This helper keeps `check_win()` small.

Its job:

- move one step at a time using `(dr, dc)`
- stop when you leave the board or hit a different color
- return the number of matching cells found

### Step 9: Implement `check_win()`

Now combine the helper and the direction list.

Before scanning, guard against invalid input:

- reject out-of-bounds coordinates
- reject coordinates whose cell does not contain the given color

Then scan across the four directions and return `True` as soon as one count reaches four.

### Step 10: Implement the `Game` constructor

Initialize:

- a new `Board`
- `player1`
- `player2`
- `current_player = player1`
- `state = GameState.IN_PROGRESS`
- `winner = None`

This gives you a valid fresh game immediately after construction.

### Step 11: Implement the `Game` getters

Add these lightweight methods next:

- `get_current_player()`
- `get_game_state()`
- `get_winner()`
- `get_board()`

They make your game easier to inspect in tests or a future UI.

### Step 12: Implement `make_move()`

This is the main orchestration method.

Recommended order:

1. reject the move if the game is already over
2. reject the move if the caller is not the current player
3. ask the board to place the disc
4. if placement failed, return `False`
5. check whether the move wins the game
6. otherwise check whether the board is full
7. otherwise switch turns
8. return `True`

The key rule here is: validate before mutating where possible.

Pseudo-code:

```python
def make_move(self, player, column: int) -> bool:
    if self.state is not GameState.IN_PROGRESS:
        return False

    if player is not self.current_player:
        return False

    row = self.board.place_disc(column, player.color)
    if row == -1:
        return False

    if self.board.check_win(row, column, player.color):
        self.state = GameState.WON
        self.winner = player
    elif self.board.is_full():
        self.state = GameState.DRAW
    else:
        self.current_player = (
            self.player2 if self.current_player is self.player1 else self.player1
        )

    return True
```

## A Good Build Order For Your First Pass

If you are implementing this for the first time, use this order:

1. enums
2. `Player`
3. `Board.__init__`
4. `Board.can_place`
5. `Board.place_disc`
6. `Board.is_full`
7. `Game.__init__`
8. `Game.make_move` with a temporary stubbed `check_win`
9. `Board._in_bounds`
10. `Board._count_in_direction`
11. `Board.check_win`
12. getters and cleanup

That order keeps the problem manageable and gives you working progress early.

## What To Test As You Go

You will move faster if you test incrementally instead of waiting until the end.

### Board tests

- placing in an empty column lands on the bottom row
- placing repeatedly in the same column stacks upward
- placing in an out-of-range column returns `-1`
- placing in a full column returns `-1`
- `is_full()` becomes `True` only when the board is completely filled

### Win detection tests

- horizontal connect four
- vertical connect four
- diagonal down-right connect four
- diagonal up-right connect four
- three in a row should not count as a win

### Game tests

- player 1 moves first
- turn alternates after a valid move
- wrong player cannot move
- moves after win or draw are rejected
- winner is recorded correctly
- draw is detected correctly

## Common Mistakes To Avoid

- putting turn logic into `Board`
- putting win-checking logic into `Game`
- storing too much logic in `Player`
- scanning the entire board after every move when you only need to inspect from the last placed disc
- using multiple boolean flags instead of a single `GameState`
- validating columns in both `Game` and `Board`, which duplicates responsibility

## How The Provided Solution Files Map To The Design

The included solution files follow the right high-level split:

- [connect_four/solution_files/player.py](connect_four/solution_files/player.py) keeps `Player` minimal
- [connect_four/solution_files/board.py](connect_four/solution_files/board.py) owns grid state, placement, and win detection
- [connect_four/solution_files/game.py](connect_four/solution_files/game.py) orchestrates turns and outcome state

That is the separation you should aim to reproduce in your own implementation.

One practical note: the provided [connect_four/solution_files/game.py](connect_four/solution_files/game.py) snippet relies on `Board` and `Player` types but does not show the imports for them, so if you run it directly you will need to add those imports yourself.

## If You Get Stuck During Implementation

When stuck, narrow the problem to one method at a time:

- first make disc placement work
- then make turn switching work
- then implement one win direction and generalize it

Do not try to solve everything at once.

## Suggested Next Step

Implement `Board` first and write a few tiny tests around `place_disc()` before you move on to `Game`. That gives you the core mechanic of the problem early and reduces debugging later.