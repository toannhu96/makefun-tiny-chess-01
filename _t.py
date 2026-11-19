import os, sys, time
os.environ["MAKEFUN_ENV_URL"] = "x"
src = open(sys.argv[1]).read().split("\nwhile True:")[0]
exec(src)


def legal_of(fen):
    B = board_of(fen)
    b = " " * 20 + "".join(" " + "".join(B.get(f + str(r), ".") for f in "abcdefgh") + " " for r in range(8, 0, -1)) + " " * 20
    bl = fen.split()[1] == "b"
    if bl:
        b = rot(b)
    def u(i):
        if bl: i = 119 - i
        return "abcdefgh"[i % 10 - 1] + str(10 - i // 10)
    out = []
    for i, j in gen(b):
        c = mv(b, i, j)[0]
        if any(c[k] == "k" for _, k in gen(c)):
            continue
        m = u(i) + u(j) + ("q" if b[i] == "P" and j < 29 else "")
        out.append(m)
    return sorted(out)


tests = [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", None),
    ("6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1", "a1a8"),
    ("r5k1/5ppp/8/8/8/8/5PPP/6K1 b - - 0 1", "a8a1"),
    ("4k3/8/8/3q4/8/8/8/3QK3 w - - 0 1", "d1d5"),
    ("4k3/P7/8/8/8/8/8/4K3 w - - 0 1", "a7a8q"),
    ("4k3/8/8/8/8/8/p7/4K3 b - - 0 1", "a2a1q"),
    ("rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w - - 2 3", None),
    ("4k3/8/8/8/3p4/8/2Q5/4K3 w - - 0 1", None),
]
for fen, want in tests:
    t = time.time()
    m = choose(fen, legal_of(fen))
    m2 = choose(fen, legal_of(fen))
    print(f"{m:6} want={want} same={m==m2} nodes={N} {time.time()-t:.1f}s")
