# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyGraphviz(PythonPackage):
    """Simple Python interface for Graphviz"""

    homepage = "https://github.com/xflr6/graphviz"
    url      = "https://pypi.io/packages/source/g/graphviz/graphviz-0.10.1.zip"

    version('0.10.1', sha256='d311be4fddfe832a56986ac5e1d6e8715d7fcb0208560da79d1bb0f72abef41f')

    variant('dev', default=False, description='development mode')
    variant('docs', default=False, description='build documentation')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-tox@3.0:', type=('build', 'run'), when='+dev')
    depends_on('py-flake8', type=('build', 'run'), when='+dev')
    depends_on('py-pep8-naming', type=('build', 'run'), when='+dev')
    depends_on('py-wheel', type=('build', 'run'), when='+dev')
    depends_on('py-twine', type=('build', 'run'), when='+dev')
    depends_on('py-mock@2:', type='test')
    depends_on('py-pytest@3.4:', type='test')
    depends_on('py-pytest-mock@1.8:', type='test')
    depends_on('py-pytest-cov', type='test')
    depends_on('py-sphinx@1.7:', type=('build', 'run'), when='+docs')
    depends_on('py-sphinx-rtd-theme', type=('build', 'run'), when='+docs')
