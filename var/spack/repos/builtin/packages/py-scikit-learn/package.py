# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitLearn(PythonPackage):
    """A set of python modules for machine learning and data mining."""

    homepage = "https://pypi.python.org/pypi/scikit-learn"
    url      = "https://pypi.io/packages/source/s/scikit-learn/scikit-learn-0.18.1.tar.gz"

    version('0.20.2', sha256='bc5bc7c7ee2572a1edcb51698a6caf11fae554194aaab9a38105d9ec419f29e6')
    version('0.20.0', sha256='97d1d971f8ec257011e64b7d655df68081dd3097322690afa1a71a1d755f8c18')
    version('0.19.1', 'b67143988c108862735a96cf2b1e827a')
    version('0.18.1', '6b0ff1eaa5010043895dd63d1e3c60c9')
    version('0.15.2', 'd9822ad0238e17b382a3c756ea94fe0d')
    version('0.16.1', '363ddda501e3b6b61726aa40b8dbdb7e')
    version('0.17.1', 'a2f8b877e6d99b1ed737144f5a478dfc')
    version('0.13.1', 'acba398e1d46274b8470f40d0926e6a4')

    depends_on('python@2.6:2.8,3.3:', when='@:0.19.1')
    depends_on('python@2.7:2.8,3.4:', when='@0.20.0:')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'), when='@:0.19.1')
    depends_on('py-numpy@1.8.2:', type=('build', 'run'), when='@0.20.0:')
    depends_on('py-scipy@0.9:', type=('build', 'run'), when='@:0.19.1')
    depends_on('py-scipy@0.13.3:', type=('build', 'run'), when='@0.20.0:')
    depends_on('py-cython@0.23:', type='build')
    depends_on('py-test@3.3.0:', type='test')
