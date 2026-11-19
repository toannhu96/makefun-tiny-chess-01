# makefun-tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/toannhu96/makefun-tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard)
[![reward](https://make.fun/badge/tiny-chess-01/toannhu96/makefun-tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01)

Alpha-beta chess engine in under 4 KB of Python, entered in [make.fun](https://make.fun/bounty/tiny-chess-01).

`main.py` is the engine, packed with `makefun compress` from `engine_src.py`.
Iterative-deepening negamax, alpha-beta, capture-first ordering, quiescence at the
leaves, and a fixed node budget instead of a clock so replays match move for move.

```sh
MAKEFUN_ENV_URL=http://store:8080 python3 main.py
```

MIT, see `LICENSE`.
