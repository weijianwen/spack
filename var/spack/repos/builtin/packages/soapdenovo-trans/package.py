# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SoapdenovoTrans(MakefilePackage):
    """SOAPdenovo-Trans is a de novo transcriptome assembler basing on the
       SOAPdenovo framework, adapt to alternative splicing and different
       expression level among transcripts."""

    homepage = "http://soap.genomics.org.cn/SOAPdenovo-Trans.html"
    url      = "https://github.com/aquaskyline/SOAPdenovo-Trans/archive/1.0.4.tar.gz"

    version('1.0.4', sha256='378a54cde0ebe240fb515ba67197c053cf95393645c1ae1399b3a611be2a9795')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('CFLAGS=         -O3 -fomit-frame-pointer -static',
                            'CFLAGS=         -O3 -fomit-frame-pointer')

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            make('127mer=1', parallel=False)

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
