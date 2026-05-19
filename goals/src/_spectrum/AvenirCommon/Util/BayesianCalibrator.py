import scipy


class BayesianCalibrator:
    """! Abstract base class for black box Bayesian calibration tools"""

    def log_likelihood(self, theta):
        """! Evaluate the log likelihood of a model for given parameter values.
        @param theta Matrix of parameter values. Rows list different parameter sets, columns list values for one parameter.
        @return a vector of log-likelihood values, one per parameter set
        """
        pass

    def log_prior(self, theta):
        """! Evaluate the prior density (on log scale) of a model for given parameter values.
        @param theta Matrix of parameter values. Rows list different parameter sets, columns list values for one parameter.
        @return a vector of prior density values on log scale, one per parameter set
        """
        pass

    def log_posterior(self, theta):
        """! Evaluate the posterior density (on log scale) of a model for given parameter values.
        @param theta Matrix of parameter values. Rows list different parameter sets, columns list values for one parameter.
        @return a vector of prior density values on log scale, one per parameter set
        """
        return self.log_likelihood(theta) + self.log_prior(theta)

    def search_mle(self, theta, lower, upper, max_iter=None, tol=None):
        """! Maximum likelihood search: Search for a maximum in the log likelihood.
        Uses Nelder-Mead simplex search with bounds constraints.
        @param theta Vector of parameter values.
        @param lower Vector of lower bounds on parameter values. Can be -Inf.
        @param upper Vector of upper bounds on parameter values. Can be +Inf.
        @param max_iter Integer. Maximum number of likelihood evaluations allowed.
        @param tol Minimum position tolerance.
        @return an scipy OptimizeResult object. See scipy documentation for details.
        """
        npar = len(theta)
        rval = scipy.optimize.minimize(
            lambda p: -self.log_likelihood(p.reshape((1, npar))),
            theta,
            method="Nelder-Mead",
            bounds=scipy.optimize.Bounds(lb=lower, ub=upper),
            tol=tol,
            options={"maxfev": max_iter},
        )
        rval.fun = -rval.fun  # we flip the sign to show the actual log-likelihood
        return rval

    def search_map(self, theta, lower, upper, max_iter=None, tol=None):
        """! Maximum a posteriori search: Search for a maximum in the log posterior density.
        Uses Nelder-Mead simplex search with bounds constraints.
        @param theta Vector of parameter values.
        @param lower Vector of lower bounds on parameter values. Can be -Inf.
        @param upper Vector of upper bounds on parameter values. Can be +Inf.
        @param max_iter Integer. Maximum number of likelihood evaluations allowed.
        @param tol Minimum position tolerance.
        @return an scipy OptimizeResult object. See scipy documentation for details.
        """
        npar = len(theta)
        rval = scipy.optimize.minimize(
            lambda p: -self.log_posterior(p.reshape((1, npar))),
            theta,
            method="Nelder-Mead",
            bounds=scipy.optimize.Bounds(lb=lower, ub=upper),
            tol=tol,
            options={"maxfev": max_iter},
        )
        rval.fun = -rval.fun  # we flip the sign to show the actual log-posterior
        return rval


# class TestFitter(BayesianCalibrator):
#     def __init__(self):
#         self.prior0 = scipy.stats.norm(loc=1.0, scale=4.0)
#         self.prior1 = scipy.stats.norm(loc=1.0, scale=4.0)
#         self.lhood0 = scipy.stats.norm(loc=0.0, scale=1.0)
#         self.lhood1 = scipy.stats.norm(loc=0.0, scale=1.0)
#
#     def log_prior(self, theta):
#         p0 = self.prior0.logpdf(theta[:,0])
#         p1 = self.prior1.logpdf(theta[:,1])
#         return p0 + p1
#
#     def log_likelihood(self, theta):
#         l0 = self.lhood0.logpdf(theta[:,0])
#         l1 = self.lhood1.logpdf(theta[:,1])
#         return l0 + l1
#
# if __name__ == "__main__":
#     theta_init = numpy.full(2, 1.0)
#     lower = numpy.full(2, -numpy.inf)
#     upper = numpy.full(2, +numpy.inf)
#
#     fitter = TestFitter()
#     res_mle = fitter.search_mle(theta_init, lower, upper) # expect res_mle.x near (0.000, 0.000)
#     res_map = fitter.search_map(theta_init, lower, upper) # expect res_map.x near (0.059, 0.059)
#
#     pass
