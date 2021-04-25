from z3 import *


def generate_constraints(program: str) -> str:
    """Generate constraints from a program of the form following the first example in the paper."""
    constraints = []
    program = program.replace("    ", "")
    lines = program.split("\n")
    guard = ""
    i = 0
    while i < len(lines):
        if "while" in lines[i]:
            if i > 0:
                entrance_var = lines[i - 1].split(":= ")
                entrance_var_val = entrance_var[1][:-1]
                entrance_constraint = (
                    "true => I["
                    + entrance_var_val
                    + "/"
                    + entrance_var[0].strip()
                    + "]"
                )
                constraints.append(entrance_constraint)
            guard = lines[i].split("(")[1].replace(")", "")[:-2]
            i += 1
            variable_unknowns = []
            while "}" not in lines[i]:
                if ":=" in lines[i]:
                    var = lines[i].split(":= ")
                    var_val = var[1][:-1]
                    var = var[0].strip()
                elif "++" in lines[i]:
                    var = lines[i][0]
                    var_val = var + " + 1"
                variable_unknowns.append("(" + var_val + ")/" + var)
                i += 1
            inductive_constraint = (
                "I \u2227 "
                + guard
                + " => "
                + "I"
                + str(variable_unknowns).replace("'", "")
            )
            constraints.append(inductive_constraint)
        if "assert" in lines[i]:
            negated_guard = ""
            if "<" in guard:
                negated_guard = ">="
            if ">" in guard:
                negated_guard = "<="
            if "!=" in guard:
                negated_guard = "=="
            assertion = lines[i].split("(")[1].replace(")", "")
            ending_constraint = (
                "I \u2227 "
                + guard[0]
                + " "
                + negated_guard
                + " "
                + guard[4:]
                + " => "
                + assertion
            )
            constraints.append(ending_constraint)
        i += 1
    return constraints


def solve_with_z3(constraints: list[str]):
    # This is all without using Farkas' lemma
    s = Solver()

    x, y, a1, a2, a3, a4, a5, a6 = Ints("x y a1 a2 a3 a4 a5 a6")
    s.add(Implies(True, Or(-50 * a1 + a2 * y + a3 >= 0, -50 * a1 + a5 * y + a6 >= 0)))
    s.add(
        Implies(
            And(Or(a1 * x + a2 * y + a3 >= 0, a4 * x + a5 * y + a6 >= 0), x < 0),
            Or(
                (x + y) * a1 + (y + 1) * a2 + a3 >= 0,
                (x + y) * a4 + (y + 1) * a5 + a6 >= 0,
            ),
        )
    )
    s.add(
        Implies(
            And(Or(a1 * x + a2 * y + a3 >= 0, a4 * x + a5 * y + a6 >= 0), x >= 0),
            y > 0,
        )
    )

    # This is using Farkas' lemma, poorly though
    # a1, a2, a3, a4, a5, a6, l1, l2, l3, l4, la, lb = Ints(
    #     "a1 a2 a3 a4 a5 a6 l1 l2 l3 l4 la lb"
    # )
    # s.add(
    #     Implies(
    #         True,
    #         And(
    #             (50 * a1 * l1) - (a3 * l1) - l1 + (50 * a4 * l2) - (a6 * l2) - l2
    #             == -la,
    #             (a2 * l1) + (a5 * l2) == 0,
    #             And(l1 >= 0, l2 >= 0, la > 0),
    #         ),
    #     )
    # )
    # # s.add((a2 * l1) + (a5 * l2) == 0)
    # # s.add(And(l1 >= 0, l2 >= 0, la > 0))
    # s.add(
    #     (2 * l3 * a1)
    #     - (a3 * l3)
    #     - l3
    #     - (a2 * l3)
    #     + (2 * l4 * a4)
    #     - (a6 * l4)
    #     - l4
    #     - (a5 * l4)
    #     == -lb
    # )
    # s.add((a2 * l3) + (a5 * l4) == 0)
    # s.add(And(l3 >= 0, l4 >= 0, lb > 0))
    s.check()
    print(s.model())


def main():
    prog1 = """
    PV1 (int y) {
        x := −50;
        while (x < 0) {
            x := x + y;
            y++;
        }
        assert(y > 0)
    }
    """

    constraints = generate_constraints(prog1)
    print(constraints)

    solve_with_z3(constraints)


if __name__ == "__main__":
    main()
