# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kripke(CMakePackage):
    """Kripke is a simple, scalable, 3D Sn deterministic particle
       transport proxy/mini app.
    """
    homepage = "https://computing.llnl.gov/projects/co-design/kripke"
    url      = "https://computing.llnl.gov/projects/co-design/download/kripke-openmp-1.1.tar.gz"

    tags = ['proxy-app']
    version('1.1', '7fe6f2b26ed983a6ce5495ab701f85bf')

    variant('mpi',    default=True, description='Build with MPI.')
    variant('openmp', default=True, description='Build with OpenMP enabled.')

    depends_on('mpi', when='+mpi')
    depends_on('cmake@3.0:', type='build')

    def cmake_args(self):
        def enabled(variant):
            return (1 if variant in self.spec else 0)

        return [
            '-DENABLE_OPENMP=%d' % enabled('+openmp'),
            '-DENABLE_MPI=%d' % enabled('+mpi'),
        ]

    def install(self, spec, prefix):
        # Kripke does not provide install target, so we have to copy
        # things into place.
        mkdirp(prefix.bin)
        install('../spack-build/kripke', prefix.bin)
