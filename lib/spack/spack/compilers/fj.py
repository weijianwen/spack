# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compiler


class Fj(spack.compiler.Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['fcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['FCC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['frt']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['frt']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'fj/fcc',
                  'cxx': 'fj/case-insensitive/FCC',
                  'f77': 'fj/frt',
                  'fc': 'fj/frt'}

    version_argument = '--version'
    version_regex = r'\((?:FCC|FRT)\) ([\d.]+)'

    @property
    def openmp_flag(self):
        return "-Kopenmp"

    @property
    def cxx98_flag(self):
        return "-std=c++98"

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def cxx14_flag(self):
        return "-std=c++14"

    @property
    def pic_flag(self):
        return "-KPIC"
