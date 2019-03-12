# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Samtools(Package):
    """SAM Tools provide various utilities for manipulating alignments in
       the SAM format, including sorting, merging, indexing and generating
       alignments in a per-position format"""

    homepage = "www.htslib.org"
    url = "https://github.com/samtools/samtools/releases/download/1.3.1/samtools-1.3.1.tar.bz2"

    version('1.9', 'cca9a40d9b91b007af2ff905cb8b5924')
    version('1.8', 'c6e981c92ca00a44656a708c4b52aba3')
    version('1.7', '2240175242b5183bfa6baf1483f68023')
    version('1.6', 'b756f05fd5d1a7042074417edb8c9aea')
    version('1.5', sha256='8542da26832ee08c1978713f5f6188ff750635b50d8ab126a0c7bb2ac1ae2df6')
    version('1.4', '8cbd7d2a0ec16d834babcd6c6d85d691')
    version('1.3.1', 'a7471aa5a1eb7fc9cc4c6491d73c2d88')
    version('1.2', '988ec4c3058a6ceda36503eebecd4122')

    depends_on('ncurses')
    # htslib became standalone @1.3.1, must use corresponding version
    depends_on('htslib@1.9',   when='@1.9')
    depends_on('htslib@1.8',   when='@1.8')
    depends_on('htslib@1.7',   when='@1.7')
    depends_on('htslib@1.6',   when='@1.6')
    depends_on('htslib@1.5',   when='@1.5')
    depends_on('htslib@1.4',   when='@1.4')
    depends_on('htslib@1.3.1', when='@1.3.1')
    depends_on('zlib')
    depends_on('bzip2')

    def install(self, spec, prefix):
        if self.spec.version >= Version('1.3.1'):
            configure('--prefix={0}'.format(prefix), '--with-ncurses',
                      'CURSES_LIB=-lncursesw')
            make()
            make('install')
        else:
            make("prefix=%s" % prefix)
            make("prefix=%s" % prefix, "install")
        # Install dev headers and libs for legacy apps depending on them
        mkdir(prefix.include)
        mkdir(prefix.lib)
        install('sam.h', prefix.include)
        install('bam.h', prefix.include)
        install('libbam.a', prefix.lib)
