# tiny-chess-01

A chess engine in at most 4,096 bytes of Python (stdlib only), entered in make.fun's
"Build the strongest chess engine in 4 KB of Python" bounty.

## What it is

`main.py` is the entrypoint the grader runs: 4,086 bytes, an LZMA stream of a readable
engine behind a small stub, so the whole engine fits the size cap. The engine inside is a
0x88 board with full legal move generation (perft-verified against python-chess), an
incremental material + piece-square-table evaluation that tracks both kings, iterative
deepening alpha-beta with a transposition table, null-move pruning, late-move reductions,
quiescence search, a mop-up term so won endgames get mated instead of stalemated, and
repetition awareness.

## How it plays

The entry speaks the competition's env protocol: it reads the position from
`MAKEFUN_ENV_URL`, searches a fixed node budget (deterministic, no wall clock), and posts
its move inside the 10-second limit.

Practice trial (trial 0 of round 33447412, the six-game gauntlet): **Elo 1191** with
2 wins, 1 draw and 3 losses, above the 1,154 practice floor the staged final requires.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8099 MAKEFUN_PROMPT_FILE=/input/prompt.txt python3 main.py
```

## License

MIT — see `LICENSE`.