# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ior(AutotoolsPackage):
    """The IOR software is used for benchmarking parallel file systems
    using POSIX, MPI-IO, or HDF5 interfaces."""

    homepage = "https://github.com/hpc/ior"
    url      = "https://github.com/hpc/ior/archive/3.2.0.tar.gz"

    version('3.2.0',    sha256='0cda0e00b7f070c6754ef8acb3873eb3a625bd8dee3f2e220291656be1322bbb')
    version('3.0.1', '71150025e0bb6ea1761150f48b553065')

    variant('hdf5',  default=False, description='support IO with HDF5 backend')
    variant('ncmpi', default=False, description='support IO with NCMPI backend')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('mpi')
    depends_on('hdf5+mpi', when='+hdf5')
    depends_on('parallel-netcdf', when='+ncmpi')

    @run_before('autoreconf')
    def bootstrap(self):
        Executable('./bootstrap')()

    def configure_args(self):
        spec = self.spec
        config_args = []

        env['CC'] = spec['mpi'].mpicc

        if '+hdf5' in spec:
            config_args.append('--with-hdf5')
            config_args.append('CFLAGS=-D H5_USE_16_API')
        else:
            config_args.append('--without-hdf5')

        if '+ncmpi' in spec:
            config_args.append('--with-ncmpi')
        else:
            config_args.append('--without-ncmpi')

        return config_args
