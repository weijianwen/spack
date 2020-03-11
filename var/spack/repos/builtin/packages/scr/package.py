# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os


class Scr(CMakePackage):
    """SCR caches checkpoint data in storage on the compute nodes of a
       Linux cluster to provide a fast, scalable checkpoint/restart
       capability for MPI codes"""

    homepage = "http://computing.llnl.gov/projects/scalable-checkpoint-restart-for-mpi"
    url      = "https://github.com/LLNL/scr/archive/v1.2.0.tar.gz"
    git      = "https://github.com/llnl/scr.git"

    version('develop', branch='develop')
    version('legacy', branch='legacy')

    version('2.0.0', sha256='471978ae0afb56a20847d3989b994fbd680d1dea21e77a5a46a964b6e3deed6b')
    version('1.2.2', sha256='764a85638a9e8762667ec1f39fa5f7da7496fca78de379a22198607b3e027847')
    version('1.2.1', sha256='23acab2dc7203e9514455a5168f2fd57bc590affb7a1876912b58201513628fe')
    version('1.2.0', sha256='e3338ab2fa6e9332d2326c59092b584949a083a876adf5a19d4d5c7a1bbae047')

    depends_on('pdsh+static_modules', type=('build', 'run'))
    depends_on('zlib')
    depends_on('mpi')

    # SCR legacy is anything 2.x.x or earlier
    # SCR components is anything 3.x.x or later
    depends_on('er', when="@3:")
    depends_on('kvtree', when="@3:")
    depends_on('rankstr', when="@3:")
    depends_on('filo', when="@3:")
    depends_on('spath', when="@3:")

    variant('dtcmp', default=True,
            description="Build with DTCMP. "
            "Necessary to enable user directory naming at runtime")
    depends_on('dtcmp', when="+dtcmp")

    variant('libyogrt', default=True,
            description="Build SCR with libyogrt for get_time_remaining.")
    depends_on('libyogrt', when="+libyogrt")

    # MySQL not yet in spack
    # variant('mysql', default=True, decription="MySQL database for logging")
    # depends_on('mysql', when="+mysql")

    variant('scr_config', default='scr.conf',
            description='Location for SCR to find its system config file. '
            'May be either absolute or relative to the install prefix')
    variant('copy_config', default='none',
            description='Location from which to copy SCR system config file. '
            'Must be an absolute path.')

    variant('fortran', default=True,
            description="Build SCR with fortran bindings")

    variant('resource_manager', default='SLURM',
            values=('SLURM', 'APRUN', 'PMIX', 'LSF', 'NONE'),
            multi=False,
            description="Resource manager for which to configure SCR.")

    variant('async_api', default='NONE',
            values=('NONE', 'CRAY_DW', 'IBM_BBAPI', 'INTEL_CPPR'),
            multi=False,
            description="Asynchronous data transfer API to use with SCR.")

    variant('file_lock', default='FLOCK',
            values=('FLOCK', 'FNCTL', 'NONE'),
            multi=False,
            description='File locking style for SCR.')

    variant('cache_base', default='/tmp',
            description='Compile time default location for checkpoint cache.')
    variant('cntl_base', default='/tmp',
            description='Compile time default location for control directory.')

    conflicts('platform=bgq')

    def get_abs_path_rel_prefix(self, path):
        # Return path if absolute, otherwise prepend prefix
        if os.path.isabs(path):
            return path
        else:
            return join_path(self.spec.prefix, path)

    def cmake_args(self):
        spec = self.spec
        args = []

        if 'platform=cray' in spec:
            args.append('-DSCR_LINK_STATIC=ON')

        args.append('-DENABLE_FORTRAN={0}'.format('+fortran' in spec))

        conf_path = self.get_abs_path_rel_prefix(
            self.spec.variants['scr_config'].value)
        args.append('-DCMAKE_SCR_CONFIG_FILE={0}'.format(conf_path))

        # We uppercase the values for these to avoid unnecessary user error.
        args.append('-DSCR_RESOURCE_MANAGER={0}'.format(
            spec.variants['resource_manager'].value.upper()))

        args.append('-DSCR_ASYNC_API={0}'.format(
            spec.variants['async_api'].value.upper()))

        args.append('-DSCR_FILE_LOCK={0}'.format(
            spec.variants['file_lock'].value.upper()))

        args.append('-DSCR_CACHE_BASE={0}'.format(
            spec.variants['cache_base'].value))

        args.append('-DSCR_CNTL_BASE={0}'.format(
            spec.variants['cntl_base'].value))

        args.append('-DWITH_PDSH_PREFIX={0}'.format(spec['pdsh'].prefix))

        if "+dtcmp" in spec:
            args.append('-DWITH_DTCMP_PREFIX={0}'.format(spec['dtcmp'].prefix))

        if "+libyogrt" in spec:
            args.append('-DWITH_YOGRT_PREFIX={0}'.format(
                spec['libyogrt'].prefix))

        # if "+mysql" in spec:
        # args.append('-DWITH_MYSQL_PREFIX={0}'.format(
        # spec['mysql'].prefix))

        return args

    @run_after('install')
    def copy_config(self):
        spec = self.spec
        if spec.variants['copy_config'].value != 'none':
            dest_path = self.get_abs_path_rel_prefix(
                spec.variants['scr_config'].value)
            install(spec.variants['copy_config'].value, dest_path)
