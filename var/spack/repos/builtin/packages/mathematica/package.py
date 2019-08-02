# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Mathematica(Package):
    """Mathematica: high-powered computation with thousands of Wolfram Language
       functions, natural language input, real-world data, mobile support.

       Note: A manual download is required for Mathematica.
       Spack will search your current directory for the download file.
       Alternatively, add this file to a mirror so that Spack can find it.
       For instructions on how to set up a mirror, see
       http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.wolfram.com/mathematica/"
    url = 'file://{0}/Mathematica_12.0.0_LINUX.sh'.format(os.getcwd())

    version('12.0.0', sha256='b9fb71e1afcc1d72c200196ffa434512d208fa2920e207878433f504e58ae9d7',
            expand=False)

    def install(self, spec, prefix):
        sh = which('sh')
        sh(self.stage.archive_file, '--', '-auto', '-verbose',
           '-targetdir={0}'.format(prefix),
           '-execdir={0}'.format(prefix.bin),
           '-selinux=y')
