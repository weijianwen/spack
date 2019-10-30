# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNotebook(PythonPackage):
    """Jupyter Interactive Notebook"""

    homepage = "https://github.com/jupyter/notebook"
    url      = "https://pypi.io/packages/source/n/notebook/notebook-4.2.3.tar.gz"

    version('4.2.3', sha256='39a9603d3fe88b60de2903680c965cf643acf2c16fb2c6bac1d905e1042b5851')
    version('4.2.2', sha256='418ba230c9b2e7e739940cae9fb4625e10a63f038e9c95cf1a9b7a244256ba38')
    version('4.2.1', sha256='a49de524dabb99f214bdf2a58f26c7892650251a23a3669c6492fb180492e197')
    version('4.2.0', sha256='e10c4916c77b48394796b5b1440d61d7b210f9941194048fe20ef88948016d84')
    version('4.1.0', sha256='b597437ba33538221008e21fea71cd01eda9da1515ca3963d7c74e44f4b03d90')
    version('4.0.6', sha256='f62e7a6afbc00bab3615b927595d27b1874cff3218bddcbab62f97f6dae567c3')
    version('4.0.4', sha256='a57852514bce1b1cf41fa0311f6cf894960cf68b083b55e6c408316b598d5648')
    version('4.0.2', sha256='8478d7e2ab474855b0ff841f693983388af8662d3af1adcb861acb900274f22a')

    variant('terminal', default=False, description="Enable terminal functionality")

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-tornado@4:', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-jupyter-console', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-nbconvert', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-ipykernel@5.1.0:', when='@4.2.0:', type=('build', 'run'))
    depends_on('py-terminado@0.3.3:', when="+terminal", type=('build', 'run'))
    depends_on('py-ipywidgets', when="+terminal", type=('build', 'run'))
