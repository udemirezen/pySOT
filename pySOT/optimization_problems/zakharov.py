import numpy as np

from .optimization_problem import OptimizationProblem


class Zakharov(OptimizationProblem):
    """Zakharov function

    Global optimum: :math:`f(0,0,...,0)=1`

    :ivar dim: Number of dimensions
    :ivar lb: Lower variable bounds
    :ivar ub: Upper variable bounds
    :ivar int_var: Integer variables
    :ivar cont_var: Continuous variables
    :ivar min: Global minimum value
    :ivar minimum: Global minimizer
    :ivar info: String with problem info
    """

    def __init__(self, dim=10):
        self.dim = dim
        self.min = 0.0
        self.minimum = np.zeros(dim)
        self.lb = -5 * np.ones(dim)
        self.ub = 10 * np.ones(dim)
        self.int_var = np.array([])
        self.cont_var = np.arange(0, dim)
        self.info = str(dim) + "-dimensional Zakharov function \n" + "Global optimum: f(0,0,...,0) = 1"

    def eval(self, x):
        """Evaluate the Zakharov function at x.

        :param x: Data point
        :type x: numpy.array
        :return: Value at x
        :rtype: float
        """
        self.__check_input__(x)
        return (
            np.sum(x ** 2)
            + np.sum(0.5 * (1 + np.arange(self.dim)) * x) ** 2
            + np.sum(0.5 * (1 + np.arange(self.dim)) * x) ** 4
        )
