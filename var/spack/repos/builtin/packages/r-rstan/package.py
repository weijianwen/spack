# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRstan(RPackage):
    """User-facing R functions are provided to parse, compile, test, estimate,
    and analyze Stan models by accessing the header-only Stan library provided
    by the 'StanHeaders' package. The Stan project develops a probabilistic
    programming language that implements full Bayesian statistical inference
    via Markov Chain Monte Carlo, rough Bayesian inference via variational
    approximation, and (optionally penalized) maximum likelihood estimation via
    optimization. In all three cases, automatic differentiation is used to
    quickly and accurately evaluate gradients without burdening the user with
    the need to derive the partial derivatives."""

    homepage = "http://mc-stan.org/"
    url      = "https://cran.r-project.org/src/contrib/rstan_2.10.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rstan"

    version('2.18.2', sha256='4d75dad95610d5a1d1c89a4ddbaf4326462e4ffe0ad28aed2129f2d9292e70ff')
    version('2.17.2', '60f4a0284c58f5efc1b1cbf488d7edda')
    version('2.10.1', 'f5d212f6f8551bdb91fe713d05d4052a')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-stanheaders', type=('build', 'run'))
    depends_on('r-inline', type=('build', 'run'))
    depends_on('r-gridextra', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
    depends_on('r-rcppeigen@0.3.3.3.0:', type=('build', 'run'), when='@2.17.2:')
    depends_on('r-bh', type=('build', 'run'))

    depends_on('r-bh@1.66:', type=('build', 'run'), when='@2.18:')
    depends_on('r-loo@2.0.0:', type=('build', 'run'), when='@2.18:')
    depends_on('r-pkgbuild', type=('build', 'run'), when='@2.18:')
    depends_on('r-stanheaders@2.18.0:', type=('build', 'run'), when='@2.18:')
    conflicts('%gcc@:4.9', when='@2.18:')
