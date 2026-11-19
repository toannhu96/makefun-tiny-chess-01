# makefun-tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/toannhu96/makefun-tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/toannhu96/makefun-tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

An alpha-beta chess engine in under 4 KB of Python, entered in
[make.fun's tiny-chess-01](https://make.fun/bounty/tiny-chess-01).

The engine is `main.py` (2,249 bytes, packed with `makefun compress`); the readable
source it is packed from is `engine_src.py` (4,063 bytes). `main.py` is the whole
program: it talks to the contest environment at `MAKEFUN_ENV_URL`, plays every game
of the gauntlet, and exits when they are over.

Search is iterative-deepening negamax with alpha-beta, a capture-first move order and
a quiescence search at the leaves. The budget is a fixed node count, never a clock,
so the same position always yields the same move and the trial's replay matches.

## Run it

```sh
MAKEFUN_ENV_URL=http://store:8080 python3 main.py
```

After any change to `engine_src.py`, re-run `makefun compress engine_src.py` and
commit the new `main.py`.

## Licence

MIT, see `LICENSE`.
