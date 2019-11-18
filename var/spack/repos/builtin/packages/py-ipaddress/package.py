# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyIpaddress(PythonPackage):
    """Python 3.3's ipaddress for older Python versions"""

    homepage = "https://github.com/phihag/ipaddress"
    url      = "https://pypi.io/packages/source/i/ipaddress/ipaddress-1.0.18.tar.gz"

    version('1.0.18', sha256='5d8534c8e185f2d8a1fda1ef73f2c8f4b23264e8e30063feeb9511d492a413e1')

    depends_on('py-setuptools', type='build')
