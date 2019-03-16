# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SofaC(MakefilePackage):
    """Standards of Fundamental Astronomy (SOFA) library for ANSI C."""

    homepage = "http://www.iausofa.org/current_C.html"
    url      = "http://www.iausofa.org/2018_0130_C/sofa_c-20180130.tar.gz"

    version('20180130', '9d6903c7690e84a788b622fba6f10146')

    @property
    def build_directory(self):
        return join_path(self.version, 'c', 'src')

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path(self.build_directory, 'makefile'))
        makefile.filter('CCOMPC = gcc', 'CCOMPC = {0}'.format(spack_cc))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.include)
            install('sofa.h', prefix.include)
            install('sofam.h', prefix.include)
            mkdir(prefix.lib)
            install('libsofa_c.a', prefix.lib)
