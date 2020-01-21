# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpywidgets(PythonPackage):
    """IPython widgets for the Jupyter Notebook"""

    homepage = "https://github.com/ipython/ipywidgets"
    url      = "https://github.com/ipython/ipywidgets/archive/5.2.2.tar.gz"

    version('5.2.2', sha256='d61ab8bb12b90981a3a6010429816d70eaa041e622043207bcb74239b664d4f3')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-ipython@4.0.0:', type=('build', 'run'))
    depends_on('py-ipykernel@4.2.2:', type=('build', 'run'))
    depends_on('py-traitlets@4.2.1:', type=('build', 'run'))
