# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cubelib(AutotoolsPackage):
    """Component of CubeBundle: General purpose C++ library and tools """

    homepage = "http://www.scalasca.org/software/cube-4.x/download.html"
    url = "http://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubelib-4.4.tar.gz"

    version('4.4.2', '843335c7d238493f1b4cb8e07555ccfe99a3fa521bf162e9d8eaa6733aa1f949')
    version('4.4',   'c903f3c44d3228ebefd00c831966988e')

    depends_on('pkgconfig', type='build')
    depends_on('zlib')

    def url_for_version(self, version):
        url = 'http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubelib-{1}.tar.gz'

        return url.format(version.up_to(2), version)

    def configure_args(self):
        configure_args = ['--enable-shared']

        return configure_args

    def install(self, spec, prefix):
        make('install', parallel=False)
