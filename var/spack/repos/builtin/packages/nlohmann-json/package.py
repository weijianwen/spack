# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NlohmannJson(CMakePackage):
    """JSON for Modern C++"""

    homepage = "https://nlohmann.github.io/json/"
    url      = "https://github.com/nlohmann/json/archive/v3.1.2.tar.gz"
    maintainers = ['ax3l']

    version('3.5.0', sha256='e0b1fc6cc6ca05706cce99118a87aca5248bd9db3113e703023d23f044995c1d')
    version('3.4.0', sha256='c377963a95989270c943d522bfefe7b889ef5ed0e1e15d535fd6f6f16ed70732')
    version('3.3.0', sha256='2fd1d207b4669a7843296c41d3b6ac5b23d00dec48dba507ba051d14564aa801')
    version('3.2.0', sha256='2de558ff3b3b32eebfb51cf2ceb835a0fa5170e6b8712b02be9c2c07fcfe52a1')
    version('3.1.2', sha256='e8fffa6cbdb3c15ecdff32eebf958b6c686bc188da8ad5c6489462d16f83ae54')
    version('3.1.1', sha256='9f3549824af3ca7e9707a2503959886362801fb4926b869789d6929098a79e47')

    variant('single_header', default=True,
        description='Use amalgamated single-header')
    variant('test', default=True,
        description='Build the tests')

    depends_on('cmake@3.8:', type='build')

    # requires mature C++11 implementations
    conflicts('%gcc@:4.7')
    # v3.3.0 adds support for gcc 4.8
    # https://github.com/nlohmann/json/releases/tag/v3.3.0
    conflicts('%gcc@:4.8', when='@:3.2.9')
    conflicts('%intel@:16')
    conflicts('%pgi@:14')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DJSON_MultipleHeaders:BOOL={0}'.format(
                'ON' if '~single_header' in spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={0}'.format(
                'ON' if '+test' in spec else 'OFF')
        ]

        return args
