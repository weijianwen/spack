# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOauthlib(PythonPackage):
    """
    A generic, spec-compliant, thorough implementation of the OAuth
    request-signing logic
    """

    homepage = "https://github.com/oauthlib/oauthlib"
    url      = "https://pypi.io/packages/source/o/oauthlib/oauthlib-3.1.0.tar.gz"

    version('3.1.0', sha256='bee41cc35fcca6e988463cacc3bcb8a96224f470ca547e697b604cc697b2f889')
    version('2.0.2', sha256='b3b9b47f2a263fe249b5b48c4e25a5bce882ff20a0ac34d553ce43cff55b53ac')

    variant('extras', default=True, description='Build with pyjwt, blinker, cryptography')

    depends_on('py-setuptools', type='build')

    depends_on('py-pyjwt@1.0.0:', type=('build', 'run'), when='+extras')
    depends_on('py-blinker',      type=('build', 'run'), when='+extras')
    depends_on('py-cryptography', type=('build', 'run'), when='+extras')

    depends_on('py-mock@2.0:', type='test')
    depends_on('py-pytest@4.0:', type='test')
    depends_on('py-pytest-cov@2.6:', type='test')

    depends_on('py-nose', type='test', when='@2.0.2')
    depends_on('py-unittest2', type='test', when='^python@2 @2.0.2')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
