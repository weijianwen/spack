# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Miniqmc(CMakePackage):
    """A simplified real space QMC code for algorithm development,
       performance portability testing, and computer science experiments
    """

    homepage = "https://github.com/QMCPACK/miniqmc"
    url      = "https://github.com/QMCPACK/miniqmc/archive/0.2.0.tar.gz"

    version('0.4.0', sha256='41ddb5de6dcc85404344c80dc7538aedf5e1f1eb0f2a67ebac069209f7dd11e4')
    version('0.3.0', sha256='3ba494ba1055df91e157cb426d1fbe4192aa3f04b019277d9e571d057664d5a9')
    version('0.2.0', 'b96bacaf48b8e9c0de05d04a95066bc1')

    tags = ['proxy-app', 'ecp-proxy-app']

    depends_on('mpi')
    depends_on('lapack')

    def cmake_args(self):
        args = [
            '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx,
            '-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc
        ]
        return args

    def install(self, spec, prefix):
        install_tree(join_path('../spack-build', 'bin'), prefix.bin)
        install_tree(join_path('../spack-build', 'lib'), prefix.lib)
