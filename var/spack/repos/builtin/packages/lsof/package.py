# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lsof(Package):
    """Lsof displays information about files open to Unix processes."""

    homepage = "https://people.freebsd.org/~abe/"
    url      = "https://www.mirrorservice.org/sites/lsof.itap.purdue.edu/pub/tools/unix/lsof/lsof_4.89.tar.gz"

    version('4.89', sha256='ff4ac555966b587f06338475c8fcc0f41402b4c8e970e730f6f83b62be8b5c0d')

    def install(self, spec, prefix):
        tar = which('tar')
        tar('xf', 'lsof_{0}_src.tar'.format(self.version))

        with working_dir('lsof_{0}_src'.format(self.version)):
            configure = Executable('./Configure')
            configure('-n', 'linux')

            make()

            mkdir(prefix.bin)
            install('lsof', prefix.bin)
