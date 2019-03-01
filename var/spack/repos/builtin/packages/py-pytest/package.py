# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytest(PythonPackage):
    """pytest: simple powerful testing with Python."""

    homepage = "http://pytest.org/"
    url      = "https://pypi.io/packages/source/p/pytest/pytest-3.7.2.tar.gz"

    import_modules = [
        '_pytest', '_pytest.assertion', '_pytest._code',
        '_pytest.mark', 'pytest'
    ]

    version('4.3.0', 'e1913b607c5c4e7d886ba6f13a43617e')
    version('3.7.2', 'd12d0d556a21fd8633e105f1a8d5a0f9')
    version('3.7.1', '2704e16bb2c11af494167f80a7cd37c4')
    version('3.5.1', 'ffd870ee3ca561695d2f916f0f0f3c0b')
    version('3.0.7', '89c60546507dc7eb6e9e40a6e9f720bd')
    version('3.0.2', '61dc36e65a6f6c11c53b1388e043a9f5')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    # Most Python packages only require setuptools as a build dependency.
    # However, pytest requires setuptools during runtime as well.
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-py@1.5.0:', type=('build', 'run'))
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-attrs@17.4.0:', type=('build', 'run'))
    depends_on('py-more-itertools@4.0.0:', type=('build', 'run'))
    depends_on('py-atomicwrites@1.0:', type=('build', 'run'))
    depends_on('py-pluggy@0.7:', when='@3.7:', type=('build', 'run'))
    depends_on('py-pluggy@0.5:0.6', when='@:3.6', type=('build', 'run'))
    depends_on('py-funcsigs', when='^python@:2', type=('build', 'run'))
    depends_on('py-pathlib2@2.2.0:', when='^python@:3.5', type=('build', 'run'))
