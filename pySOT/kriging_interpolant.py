#!/usr/bin/env python
"""
.. module:: kriging_interpolant
   :synopsis: kriging model interpolation
.. moduleauthor:: Yi Shen <ys623@cornell.edu>

:Module: kriging_interpolant
:Author: Yi Shen <ys623@cornell.edu>
"""

import numpy as np
from pyKriging.krige import kriging


class KrigingInterpolant(kriging):
    """Compute and evaluate Kriging interpolant.

    :ivar nump: Current number of points
    :ivar maxp: Initial maximum number of points (can grow)
    :ivar initp: Number of initial point for setting up Kriging model
    :ivar setup: Flag that indicates whether a Kriging model is created or not
    :ivar x: Interpolation points
    :ivar fx: Function evaluations of interpolation points
    :ivar k: Kriging model instance
    :ivar updated: Flag that indicates whether a Kriging
        model is up-to-date or not
    """

    def __init__(self, initp=10, maxp=100):
        self.nump = 0
        self.maxp = maxp
        self.initp = initp
        self.x = None
        self.fx = None
        self.dim = None
        self.k = None
        self.updated = None

    def reset(self):
        """
        Reset the Kriging interpolant
        """
        self.nump = 0
        self.x = None
        self.fx = None

    def _alloc(self, dim):
        """
        Allocate storage for x, fx and rhs.

        :param dim: Number of dimensions
        """
        maxp = self.maxp
        self.dim = dim
        self.x = np.zeros((maxp, dim))
        self.fx = np.zeros((maxp, 1))

    def _realloc(self, dim, extra=1):
        """
        Expand allocation to accommodate more points (if needed)

        :param dim: Number of dimensions
        :param extra: Number of additional points to accommodate
        """
        if self.nump == 0:
            self._alloc(dim)
        elif self.nump + extra > self.maxp:
            self.maxp = max(self.maxp*2, self.maxp+extra)
            self.x.resize((self.maxp, dim))
            self.fx.resize((self.maxp, 1))

    def _model(self):
        """
        Create Kriging model
        """
        self.k = kriging(self.x[:self.nump+1, :],
                         self.fx[:self.nump+1, :], self.maxp)
        self.k.train()

    def get_x(self):
        """
        Get the list of data points

        :return: List of data points
        """
        return self.x[:self.nump, :]

    def get_fx(self):
        """
        Get the list of function values for the data points.

        :return: List of function values
        """
        return self.fx[:self.nump, :]

    def add_point(self, xx, fx):
        """
        Add a new function evaluation

        :param xx: Point to add
        :param fx: The function value of the point to add
        """
        dim = len(xx)
        self._realloc(dim)
        self.x[self.nump, :] = xx
        self.fx[self.nump, :] = fx
        self.nump += 1
        if self.nump < self.initp:
            # print('collecting initial points for setup')
            pass
        elif self.nump == self.initp:
            # set up initial Kriging model
            # print('using initial points for setup')
            self._model()
        else:
            # add point to kriging model
            # print('adding a point to Kriging model!')
            self.k.addPoint(xx, fx)
            self.updated = True

    def eval(self, xx):
        """
        Evaluate the Kriging interpolant at the point xx

        :param xx: Point where to evaluate
        :return: Value of the Kriging interpolant at x
        """
        if self.updated:
            self.k.train()
        self.updated = False
        fx = self.k.predict(xx.ravel())
        return fx

    def evals(self, xx):
        """
        Evaluate the Kriging interpolant at the points xx

        :param xx: Points where to evaluate
        :return: Values of the Kriging interpolant at x
        """
        length = xx.shape[0]
        fx = np.zeros(shape=(1, length))
        for i in range(length):
            fx[0, i] = self.eval(np.asarray(xx[i]))
        return fx.ravel()

    def deriv(self, x):
        """
        Evaluate the derivative of the rbf interpolant at x

        :param x: Data point
        :return: Derivative of the rbf interpolant at x
        """
        # FIXME, To be implemented
        raise NotImplementedError

# ====================================================================


def _main():
    """Main test routine"""

    def test_f(x):
        """Test function"""
        fx = x[1]*np.sin(x[0]) + x[0]*np.cos(x[1])
        return fx

    fhat = KrigingInterpolant(20, 50)
    print("fhat.initp: %i , fhat.maxp: %i" % (fhat.initp, fhat.maxp))

    # Set up more points
    xs = np.random.rand(50, 2)
    for i in range(40):
        xx = xs[i, :]
        fx = test_f(xx)
        fhat.add_point(xx, fx)
    fhx = fhat.evals(xs[:10, :])
    for i in range(10):
        fx = test_f(xs[i, :])
        print("Err: %e" % (np.abs(fx-fhx[i])/np.abs(fx)))


if __name__ == "__main__":
    _main()
