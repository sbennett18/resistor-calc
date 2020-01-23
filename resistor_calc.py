from itertools import product
import re

BOUND = re.compile(r"^(?P<expr>.+?)(?P<op>[<>!]?[=~]+)(?P<trg>.+?)$")

POWERS = range(7)
E3 = {1.0, 2.2, 4.7}
E3_EXPANDED = tuple(x * pow(10, p) for x, p in product(E3, POWERS))

rcalc = (E3_EXPANDED, E3_EXPANDED)
print(E3_EXPANDED)

bounds = ("R1 + R2 <= 10e3", "1.2 * R2 / (R1 + R2) ~ 0.6")

OPS = {
    "<=": lambda expr, trg: expr <= trg,
    "<": lambda expr, trg: expr < trg,
    ">=": lambda expr, trg: expr >= trg,
    ">": lambda expr, trg: expr > trg,
    "==": lambda expr, trg: expr == trg,
    "!=": lambda expr, trg: expr != trg,
    "~": lambda expr, trg: abs(expr - trg),
}


def split_bound(bound):
    expr, op, trg = map(str.strip, BOUND.fullmatch(bound).groups())
    return (expr, lambda expr: OPS[op](expr, float(trg)))


cmp_bounds = tuple(map(split_bound, bounds))
for bound in cmp_bounds:
    print(bound)

combinations = []
# TODO Is there a better way to do this?
for rset in product(*rcalc):
    ctx = {f"R{i}": v for i, v in enumerate(rset, 1)}
    err = 0.0

    for expr, fbound in cmp_bounds:
        result = fbound(eval(expr, None, ctx))
        # TODO Especially this break/continue section?
        if result is False:
            err = None
            break
        elif result is True:
            continue
        else:
            err += result

    combinations.append((err, ctx))

print("Number of combinations:", len(combinations))

for err, ctx in sorted(
    filter(lambda t: t[0] is not None, combinations), key=lambda t: t[0]
)[:15]:
    print(f"{err:.5}", ctx)
