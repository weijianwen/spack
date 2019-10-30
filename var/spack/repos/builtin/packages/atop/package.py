# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Atop(Package):
    """Atop is an ASCII full-screen performance monitor for Linux"""
    homepage = "http://www.atoptool.nl/index.php"
    url      = "http://www.atoptool.nl/download/atop-2.2-3.tar.gz"

    version('2.2-3', sha256='c785b8a2355be28b3de6b58a8ea4c4fcab8fadeaa57a99afeb03c66fac8e055d')

    depends_on('zlib')
    depends_on('ncurses')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install("atop", join_path(prefix.bin, "atop"))
        mkdirp(join_path(prefix.man, "man1"))
        install(join_path("man", "atop.1"),
                join_path(prefix.man, "man1", "atop.1"))
