# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apex(CMakePackage):
    """Autonomic Performance Environment for eXascale (APEX)."""

    homepage = "http://github.com/khuck/xpress-apex"
    url      = "http://github.com/khuck/xpress-apex/archive/v0.1.tar.gz"

    version('0.1', sha256='bb0be37f8f8133fe492998515bcf66a4df452c28a995d317228fbed9b18e6a92')

    depends_on("binutils+libiberty")
    depends_on("boost@1.54:")
    depends_on('cmake@2.8.12:', type='build')
    depends_on("activeharmony@4.5:")
    depends_on("ompt-openmp")

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBOOST_ROOT=%s' % spec['boost'].prefix,
            '-DUSE_BFD=TRUE',
            '-DBFD_ROOT=%s' % spec['binutils'].prefix,
            '-DUSE_ACTIVEHARMONY=TRUE',
            '-DACTIVEHARMONY_ROOT=%s' % spec['activeharmony'].prefix,
            '-DUSE_OMPT=TRUE',
            '-DOMPT_ROOT=%s' % spec['ompt-openmp'].prefix,
        ]
