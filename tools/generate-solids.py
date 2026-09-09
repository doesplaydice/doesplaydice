import math, itertools

PHI = (1 + 5 ** 0.5) / 2

def signs(*vals):
    """All sign combinations of the non-zero coordinates."""
    out = set()
    for flips in itertools.product([1, -1], repeat=len(vals)):
        out.add(tuple(v * f for v, f in zip(vals, flips)))
    return out

def perms_even(t):
    """Even cyclic permutations."""
    a, b, c = t
    return [(a, b, c), (b, c, a), (c, a, b)]

def build(name):
    if name == "tetrahedron":
        return [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]
    if name == "hexahedron":
        return sorted(signs(1,1,1))
    if name == "octahedron":
        v = set()
        for p in perms_even((1,0,0)):
            v |= {p, tuple(-x for x in p)}
        return sorted(v)
    if name == "dodecahedron":
        v = set(signs(1,1,1))
        for base in perms_even((0, 1/PHI, PHI)):
            v |= signs(*base) if 0 not in base else set()
        # the (0, ±1/phi, ±phi) family needs explicit handling (a zero coord)
        for p in perms_even((0, 1/PHI, PHI)):
            i0 = p.index(0)
            for s1 in (1,-1):
                for s2 in (1,-1):
                    q = list(p)
                    nz = [i for i in range(3) if i != i0]
                    q[nz[0]] *= s1; q[nz[1]] *= s2
                    v.add(tuple(q))
        return sorted(v)
    if name == "icosahedron":
        v = set()
        for p in perms_even((0, 1, PHI)):
            i0 = p.index(0)
            for s1 in (1,-1):
                for s2 in (1,-1):
                    q = list(p)
                    nz = [i for i in range(3) if i != i0]
                    q[nz[0]] *= s1; q[nz[1]] *= s2
                    v.add(tuple(q))
        return sorted(v)
    raise ValueError(name)

def edges_of(verts):
    """Edges = vertex pairs at the minimum pairwise distance."""
    d = lambda a, b: math.dist(a, b)
    dists = [d(a, b) for a, b in itertools.combinations(verts, 2)]
    m = min(dists)
    return [(i, j) for (i, a), (j, b) in itertools.combinations(enumerate(verts), 2)
            if abs(d(a, b) - m) < 1e-6]

EXPECTED = {  # Euler: V - E + F = 2
    "tetrahedron":  (4, 6, 4),
    "hexahedron":   (8, 12, 6),
    "octahedron":   (6, 12, 8),
    "dodecahedron": (20, 30, 12),
    "icosahedron":  (12, 30, 20),
}

for name, (ev, ee, ef) in EXPECTED.items():
    v = build(name); e = edges_of(v)
    okv, oke = len(v) == ev, len(e) == ee
    euler = len(v) - len(e) + ef
    print("  %-13s V=%-3d(%s) E=%-3d(%s)  V-E+F=%d %s"
          % (name, len(v), "ok" if okv else "BAD", len(e), "ok" if oke else "BAD",
             euler, "ok" if euler == 2 else "BAD"))

# ---------------------------------------------------------------- projection
def rot(v, ax, ay):
    x, y, z = v
    ca, sa = math.cos(ax), math.sin(ax)
    y, z = y * ca - z * sa, y * sa + z * ca
    cb, sb = math.cos(ay), math.sin(ay)
    x, z = x * cb + z * sb, -x * sb + z * cb
    return (x, y, z)

def svg_for(name, ax_deg, ay_deg, size=120, pad=9):
    verts = build(name)
    eds = edges_of(verts)
    R = [rot(v, math.radians(ax_deg), math.radians(ay_deg)) for v in verts]
    scale = max(math.hypot(x, y) for x, y, _ in R)
    zs = [z for _, _, z in R]
    zmin, zmax = min(zs), max(zs)
    half = size / 2
    usable = half - pad

    def P(p):
        x, y, _ = p
        return (half + x / scale * usable, half - y / scale * usable)

    parts = []
    # circumscribed construction circle -- the Kepler nod
    parts.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="currentColor" '
                 'stroke-width=".4" opacity=".18"/>' % (half, half, usable))
    # edges, back ones fainter
    for i, j in eds:
        zm = (R[i][2] + R[j][2]) / 2
        t = 0 if zmax == zmin else (zm - zmin) / (zmax - zmin)
        op = 0.30 + 0.70 * t
        (x1, y1), (x2, y2) = P(R[i]), P(R[j])
        parts.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="currentColor" '
                     'stroke-width="1.05" stroke-linecap="round" opacity="%.2f"/>'
                     % (x1, y1, x2, y2, op))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
            'aria-label="%s, one of the five Platonic solids">%s</svg>'
            % (size, size, name.capitalize(), "".join(parts)))

VIEWS = {  # tuned so each solid reads clearly rather than edge-on
    "tetrahedron":  (-14, 28),
    "hexahedron":   (-18, 32),
    "octahedron":   (-12, 24),
    "dodecahedron": (-16, 20),
    "icosahedron":  (-14, 30),
}
import os
out = "wiki/docs/assets/img"
os.makedirs(out, exist_ok=True)
for n, (ax, ay) in VIEWS.items():
    s = svg_for(n, ax, ay)
    open(os.path.join(out, "solid-%s.svg" % n), "w").write(s)
    print("  solid-%-13s %5d bytes  %2d edges" % (n + ".svg", len(s), len(edges_of(build(n)))))
