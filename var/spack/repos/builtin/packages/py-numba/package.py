# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumba(PythonPackage):
    """NumPy aware dynamic Python compiler using LLVM"""

    homepage = "https://numba.pydata.org/"
    url      = "https://pypi.io/packages/source/n/numba/numba-0.35.0.tar.gz"

    version('0.40.1', sha256='52d046c13bcf0de79dbfb936874b7228f141b9b8e3447cc35855e9ad3e12aa33')
    version('0.35.0', '4f447383406f54aaf18ffaba3a0e79e8')

    depends_on('python@3.3:3.7.9999', type=('build', 'run'), when='@0.40.1:')
    depends_on('python@3.3:3.6.9999', type=('build', 'run'), when='@:0.35.0')
    depends_on('py-numpy@1.10:1.99', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # Note: As of 1 Nov 2018, 0.25 was the latest version of py-llvmlite.
    # That's why it was chosen as an upper bound in the following depends_on
    # calls.  If newer versions maintain backwards compatibility, the calls
    # can be updated accordingly.
    depends_on('py-llvmlite@0.25:', type=('build', 'run'), when='@0.40.1:')
    depends_on('py-llvmlite@0.20:0.25', type=('build', 'run'), when='@0.35.1')

    depends_on('py-argparse', type=('build', 'run'))
    depends_on('py-funcsigs', type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-singledispatch', type=('build', 'run'), when='^python@:3.3.99')

    # Version 6.0.0 of llvm had a hidden symbol which breaks numba at runtime.
    # See https://reviews.llvm.org/D44140
    conflicts('^llvm@6.0.0')
