# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScandir(PythonPackage):
    """scandir, a better directory iterator and faster os.walk()."""

    homepage = "https://github.com/benhoyt/scandir"
    url      = "https://pypi.io/packages/source/s/scandir/scandir-1.9.0.tar.gz"

    import_modules = ['scandir']

    version('1.9.0', sha256='44975e209c4827fc18a3486f257154d34ec6eaec0f90fef0cca1caa482db7064')
    version('1.6',   sha256='e0278a2d4bc6c0569aedbe66bf26c8ab5b2b08378b3289de49257f23ac624338')

    depends_on('py-setuptools', type=('build'))
