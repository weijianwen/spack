# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOset(PythonPackage):
    """Set that remembers original insertion order."""

    homepage = "https://pypi.python.org/pypi/oset"
    url      = "https://pypi.io/packages/source/o/oset/oset-0.1.3.tar.gz"

    import_modules = ['oset']

    version('0.1.3', sha256='4c1fd7dec96eeff9d3260995a8e37f9f415d0bdb79975f57824e68716ac8f904')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.5:', type=('build', 'run'))
