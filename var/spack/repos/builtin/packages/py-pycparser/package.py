# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycparser(PythonPackage):
    """A complete parser of the C language, written in pure python."""

    homepage = "https://github.com/eliben/pycparser"
    url      = "https://pypi.io/packages/source/p/pycparser/pycparser-2.19.tar.gz"

    import_modules = ['pycparser', 'pycparser.ply']

    version('2.19', sha256='a988718abfad80b6b157acce7bf130a30876d27603738ac39f140993246b25b3')
    version('2.18', sha256='99a8ca03e29851d96616ad0404b4aad7d9ee16f25c9f9708a11faf2810f7b226')
    version('2.17', sha256='0aac31e917c24cb3357f5a4d5566f2cc91a19ca41862f6c3c22dc60a629673b6')
    version('2.13', sha256='b399599a8a0e386bfcbc5e01a38d79dd6e926781f9e358cd5512f41ab7d20eb7')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
