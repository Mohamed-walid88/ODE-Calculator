from sympy import *

# Define symbols globally
x = Symbol('x')
y = Function('y')(x)

def solving_ode(eq):
    def non_exact(eq):
        if not (isinstance(eq, Eq) and eq.rhs == 0):
            return None, None

        expr = eq.lhs
        M = expr.coeff(Derivative(x))
        N = expr.coeff(Derivative(y))

        if M is None or N is None:
            return None, None

        expr1 = simplify((M.diff(y) - N.diff(x)) / N)
        if expr1.free_symbols == {x}:
            mu = exp(integrate(expr1, x))
        else:
            expr2 = simplify((N.diff(x) - M.diff(y)) / M)
            if expr2.free_symbols == {y}:
                mu = exp(integrate(expr2, y))
            else:
                return None, None

        new_eq = Eq(mu * M * Derivative(x) + mu * N * Derivative(y), 0)
        return new_eq, '1st_exact'

    def solve_homogeneous(eq):
        try:
            dy_dx = solve(eq, Derivative(y, x))[0]
        except Exception:
            return None

        v = Function('v')(x)
        y_sub = x * v
        dy_sub = diff(x * v, x)

        # Substitute y = x*v and dy/dx accordingly
        new_eq = Eq(dy_sub, dy_dx.subs({y: y_sub}))
        try:
            sol_v = dsolve(new_eq, v)
            sol_y = sol_v.subs(v, y / x)
            return sol_y
        except Exception:
            return None

    # Classify ODE
    classifying = classify_ode(eq)

    if 'homogeneous' not in classifying:
        try:
            dy_dx = solve(eq, Derivative(y, x))[0]
            v = symbols('v')
            substituted = simplify(dy_dx.subs(y, v * x))
            if not substituted.has(x):
                classifying.append('homogeneous')
        except Exception:
            pass

    method_map = {
        'separable': 'separable',
        'homogeneous': 'homogeneous',
        '1st_exact': 'exact',
        '1st_exact_integrating_factor': 'reduced to exact by integrating factor',
        '1st_linear': 'linear',
        'almost_linear': 'transformed to linear',
        'Bernoulli': 'Bernoulli',
        'nth_linear_constant_coeff_homogeneous': 'homogeneous',
        'nth_linear_constant_coeff_undetermined_coefficients': 'non-homogeneous',
        'nth_linear_constant_coeff_variation_of_parameters': 'variation of parameters',
        'separable_parallel' : 'separable'
    }

    preferred_order = [
        'Bernoulli',
        '1st_linear',
        'separable',
        'almost_linear',
        'homogeneous',
        '1st_exact',
        '1st_exact_integrating_factor',
        'nth_linear_constant_coeff_homogeneous',
        'nth_linear_constant_coeff_undetermined_coefficients',
        'nth_linear_constant_coeff_variation_of_parameters'
    ]

    readable_classes = []
    solution = None

    for method in preferred_order:
        if method in classifying:
            readable_classes.append(method_map[method])
            if solution is None:
                try:
                    solution = dsolve(eq, hint=method, simplify=False)
                except Exception:
                    if method == 'homogeneous':
                        solution = solve_homogeneous(eq)

    if solution is None:
        ex, type1 = non_exact(eq)
        if ex is not None:
            readable_classes.append(type1)
            try:
                solution = dsolve(ex, hint=type1, simplify=False)
            except Exception:
                print("Invalid equation; unable to solve.")

    return solution.subs(y, 'y'), readable_classes