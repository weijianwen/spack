# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import re


class Kahip(SConsPackage):
    """KaHIP - Karlsruhe High Quality Partitioning - is a family of graph
    partitioning programs. It includes KaFFPa (Karlsruhe Fast Flow
    Partitioner), which is a multilevel graph partitioning algorithm,
    in its variants Strong, Eco and Fast, KaFFPaE (KaFFPaEvolutionary)
    which is a parallel evolutionary algorithm that uses KaFFPa to
    provide combine and mutation operations, as well as KaBaPE which
    extends the evolutionary algorithm. Moreover, specialized
    techniques are included to partition road networks (Buffoon), to
    output a vertex separator from a given partition or techniques
    geared towards efficient partitioning of social networks.
    """

    homepage  = 'http://algo2.iti.kit.edu/documents/kahip/index.html'
    url       = 'http://algo2.iti.kit.edu/schulz/software_releases/KaHIP_2.00.tar.gz'
    git       = 'https://github.com/schulzchristian/KaHIP.git'

    version('develop', branch='master')
    version('2.00', sha256='1cc9e5b12fea559288d377e8b8b701af1b2b707de8e550d0bda18b36be29d21d')

    depends_on('argtable')
    depends_on('mpi')  # Note: upstream package only tested on openmpi

    conflicts('%clang')

    def patch(self):
        """Internal compile.sh scripts hardcode number of cores to build with.
        Filter these out so Spack can control it."""

        files = [
            'compile.sh',
            'parallel/modified_kahip/compile.sh',
            'parallel/parallel_src/compile.sh',
        ]

        for f in files:
            filter_file('NCORES=.*', 'NCORES={0}'.format(make_jobs), f)

    def build(self, spec, prefix):
        """Build using the KaHIP compile.sh script. Uses scons internally."""
        builder = Executable('./compile.sh')
        builder()

    def install(self, spec, prefix):
        """Install under the prefix"""
        # Ugly: all files land under 'deploy' and we need to disentangle them
        mkdirp(prefix.bin)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        with working_dir('deploy'):
            for f in os.listdir('.'):
                if re.match(r'.*\.(a|so|dylib)$', f):
                    install(f, prefix.lib)
                elif re.match(r'.*\.h$', f):
                    install(f, prefix.include)
                else:
                    install(f, prefix.bin)
