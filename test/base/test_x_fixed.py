"""Test the fixing of parameters feature."""

import numpy as np

import pypesto
import pypesto.optimize

from ..util import rosen_for_sensi


def test_problem():
    problem = create_problem()

    assert len(problem.lb) == 3
    assert problem.dim == 3
    assert problem.dim_full == 5
    assert np.array_equal(problem.x_free_indices, [0, 2, 4])


def test_optimize():
    problem = create_problem()
    optimizer = pypesto.optimize.ScipyOptimizer()
    n_starts = 5
    result = pypesto.optimize.minimize(
        problem=problem,
        optimizer=optimizer,
        n_starts=n_starts,
        filename=None,
        progress_bar=False,
    )

    optimizer_result = result.optimize_result.list[0]
    assert len(optimizer_result.x) == 5
    assert len(optimizer_result.grad) == 5

    # maybe not what we want, but that's how it is right now
    assert len(problem.ub) == 3

    # nans written into unknown components
    assert np.isnan(optimizer_result.grad[1])

    # fixed values written into parameter vector
    assert optimizer_result.x[1] == 1

    lb_full = problem.get_full_vector(problem.lb)
    assert len(lb_full) == 5


def create_problem():
    objective = rosen_for_sensi(2)['obj']
    lb = [-3, -3, -3, -3, -3]
    ub = [3, 3, 3, 3, 3]
    x_fixed_indices = [1, 3]
    x_fixed_vals = [1, 1]
    problem = pypesto.Problem(
        objective=objective,
        lb=lb,
        ub=ub,
        x_fixed_indices=x_fixed_indices,
        x_fixed_vals=x_fixed_vals,
    )

    return problem
