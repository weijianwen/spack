# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Extension2(Package):
    """A package which extends another package. It also depends on another
       package which extends the same package."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/extension2-1.0.tar.gz"

    extends('extendee')
    depends_on('extension1', type=('build', 'run'))

    version('1.0', 'hash-extension2-1.0')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with open(os.path.join(prefix.bin, 'extension2'), 'w+') as fout:
            fout.write(str(spec.version))
