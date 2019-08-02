# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
from spack import *


class Leveldb(CMakePackage):
    """LevelDB is a fast key-value storage library written at Google
    that provides an ordered mapping from string keys to string values."""

    homepage = "https://github.com/google/leveldb"
    url      = "https://github.com/google/leveldb/archive/1.22.tar.gz"
    git      = "https://github.com/google/leveldb.git"

    version('master', branch='master')
    version('1.22', '55423cac9e3306f4a9502c738a001e4a339d1a38ffbee7572d4a07d5d63949b2')
    version('1.20', '298b5bddf12c675d6345784261302252')
    version('1.18', '73770de34a2a5ab34498d2e05b2b7fa0')

    variant('shared', default=True, description='Build shared library')

    depends_on('cmake@3.9:', when='@1.21:', type='build')

    depends_on('snappy')

    def url_for_version(self, version):
        url = 'https://github.com/google/leveldb/archive/{0}.tar.gz'

        if version >= Version('1.21'):
            ver = version
        else:
            ver = 'v{0}'.format(version)

        return url.format(ver)

    # CMake support was added in version 1.21
    @when('@:1.20')
    def cmake(self, spec, prefix):
        pass

    @when('@:1.20')
    def build(self, spec, prefix):
        pass

    @when('@:1.20')
    def install(self, spec, prefix):
        make()

        mkdirp(prefix.lib)

        # Needed for version 1.20
        libraries  = glob.glob('out-shared/libleveldb.*')
        libraries += glob.glob('out-static/libleveldb.*')
        # Needed for version 1.18
        libraries += glob.glob('libleveldb.*')

        for library in libraries:
            install(library, prefix.lib)

        install_tree('include', prefix.include)

    def cmake_args(self):
        args = []

        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        return args

    @run_after('install')
    def install_pkgconfig(self):
        libdir = self.spec['leveldb'].libs.directories[0]
        pkg_path = join_path(libdir, 'pkgconfig')
        mkdirp(pkg_path)

        with open(join_path(pkg_path, 'leveldb.pc'), 'w') as f:
            f.write('prefix={0}\n'.format(self.prefix))
            f.write('exec_prefix=${prefix}\n')
            f.write('libdir={0}\n'.format(libdir))
            f.write('includedir={0}\n'.format(self.prefix.include))
            f.write('\n')
            f.write('Name: leveldb\n')
            f.write('Description: LevelDB is a fast key-value storage library'
                    ' written at Google that provides an ordered mapping from'
                    ' string keys to string values.\n')
            f.write('Version: {0}\n'.format(self.spec.version))
            f.write('Cflags: -I${includedir}\n')
            f.write('Libs: -L${libdir} -lleveldb\n')
