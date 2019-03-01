# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPeriodictable(PythonPackage):
    """nose extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://pypi.python.org/pypi/periodictable"
    url      = "https://pypi.io/packages/source/p/periodictable/periodictable-1.4.1.tar.gz"

    version('1.5.0', sha256='b020c04c6765d21903e4604a76ca33cda98677003fe6eb48ed3690cfb03253b2')
    version('1.4.1', '7246b63cc0b6b1be6e86b6616f9e866e')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyparsing', type=('build', 'run'))
