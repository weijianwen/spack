# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libnetworkit(CMakePackage):
    """NetworKit is a growing open-source toolkit for large-scale network
       analysis. Its aim is to provide tools for the analysis of large networks
       in the size range from thousands to billions of edges. For this purpose,
       it implements efficient graph algorithms, many of them parallel to
       utilize multicore architectures. These are meant to compute standard
       measures of network analysis, such as degree sequences, clustering
       coefficients, and centrality measures. In this respect, NetworKit is
       comparable to packages such as NetworkX, albeit with a focus on
       parallelism and scalability."""

    homepage = "https://networkit.github.io/"
    url      = "https://github.com/networkit/networkit/archive/6.1.tar.gz"

    maintainers = ['fabratu']

    version('6.1', sha256='22c953ea1054c356663b31c77114c2f0c8fec17e0e707aeec23026241beab9b2')

    variant('static', default=False, description='Enables the build of shared libraries')
    variant('doc', default=False, description='Enables the build with sphinx documentation')

    depends_on('libtlx')
    depends_on('py-sphinx', when='+doc', type='build')

    patch('0001-Name-agnostic-import-of-tlx-library.patch', when='@6.1')

    def cmake_args(self):
        spec = self.spec

        tlx_libs = spec['libtlx'].prefix

        args = ['-DNETWORKIT_EXT_TLX=%s' % tlx_libs,
                '-DNETWORKIT_STATIC=%s' %
                ('ON' if '+static' in spec else 'OFF')]

        return args
