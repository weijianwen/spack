# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from spack import *
from spack.operating_systems.mac_os import macos_version

#
# Need to add:
#  KOKKOS support using an external (i.e. spack-supplied) kokkos library.
#  Data Warehouse (FAODEL) enable/disable


class Seacas(CMakePackage):
    """The SEACAS Project contains the Exodus and IOSS libraries and a
     collection of applications which create, query, modify, or
     translate exodus databases.  Default is to build the exodus and
     IOSS libraries and the io_shell, io_info, struc_to_unstruc apps.
    """
    homepage = "http://gsjaardema.github.io/seacas/"
    git      = "https://github.com/gsjaardema/seacas.git"

    maintainers = ['gsjaardema']

    # ###################### Versions ##########################
    version('master', branch='master')

    # ###################### Variants ##########################
    # Package options
    # The I/O libraries (exodus, IOSS) are always built
    # -- required of both applications and legacy variants.
    variant('applications', default=True,
            description='Build all "current" SEACAS applications. This'
            ' includes a debatable list of essential applications: '
            'aprepro, conjoin, ejoin, epu, exo2mat, mat2exo, '
            'exo_format, exodiff, explore, grepos, '
            'nemslice, nemspread')
    variant('legacy', default=True,
            description='Build all "legacy" SEACAS applications. This includes'
            ' a debatable list of "legacy" applications: algebra, blot, '
            'exomatlab, exotxt, fastq, gen3d, genshell, gjoin, mapvar, '
            'mapvar-kd, numbers, txtexo, nemesis')

    # Build options
    variant('fortran',      default=True,
            description='Compile with Fortran support')
    variant('shared',       default=True,
            description='Enables the build of shared libraries')
    variant('mpi', default=True, description='Enables MPI parallelism.')

    variant('thread_safe',  default=False,
            description='Enable thread-safe exodus and IOSS libraries')

    # TPLs (alphabet order)
    variant('cgns',         default=True,
            description='Enable CGNS')
    variant('matio',        default=True,
            description='Compile with matio (MatLab) support')
    variant('metis',        default=False,
            description='Compile with METIS and ParMETIS')
    variant('x11',          default=True,
            description='Compile with X11')

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)

    depends_on('netcdf@4.6.2:+mpi+parallel-netcdf', when='+mpi')
    depends_on('netcdf@4.6.2:~mpi', when='~mpi')
    depends_on('cgns@develop+mpi+scoping', when='+cgns +mpi')
    depends_on('cgns@develop~mpi+scoping', when='+cgns ~mpi')
    depends_on('matio', when='+matio')
    depends_on('metis+int64+real64', when='+metis ~mpi')
    depends_on('parmetis+int64+real64', when='+metis +mpi')

    # MPI related dependencies
    depends_on('mpi', when='+mpi')

    depends_on('cmake@3.1:', type='build')

    def cmake_args(self):
        spec = self.spec

        options = []

        # #################### Base Settings #######################

        if '+mpi' in spec:
            options.extend([
                '-DCMAKE_C_COMPILER=%s'       % spec['mpi'].mpicc,
                '-DCMAKE_CXX_COMPILER=%s'     % spec['mpi'].mpicxx,
                '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
                '-DTPL_ENABLE_MPI:BOOL=ON',
                '-DMPI_BASE_DIR:PATH=%s'      % spec['mpi'].prefix,
            ])

        options.extend([
            '-DSEACASProj_ENABLE_TESTS:BOOL=ON',
            '-DSEACASProj_ENABLE_CXX11:BOOL=ON',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DSEACASProj_ENABLE_Kokkos:BOOL=OFF',
            '-DSEACASProj_HIDE_DEPRECATED_CODE:BOOL=OFF',
            '-DSEACASExodus_ENABLE_THREADSAFE:BOOL=%s' % (
                'ON' if '+thread_safe' in spec else 'OFF'),
            '-DSEACASIoss_ENABLE_THREADSAFE:BOOL=%s' % (
                'ON' if '+thread_safe' in spec else 'OFF'),
            '-DSEACASProj_ENABLE_Fortran:BOOL=%s' % (
                'ON' if '+fortran' in spec else 'OFF'),
            '-DTPL_ENABLE_X11:BOOL=%s' % (
                'ON' if '+x11' in spec else 'OFF'),
        ])

        # ########## What applications should be built #############
        # Check whether they want everything; if so, do the easy way...
        if '+applications' in spec and '+legacy' in spec:
            options.extend([
                '-DSEACASProj_ENABLE_ALL_PACKAGES:BOOL=ON',
                '-DSEACASProj_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON',
                '-DSEACASProj_ENABLE_SECONDARY_TESTED_CODE:BOOL=ON',
            ])
        else:
            # Don't want everything; handle the subsets:
            options.extend([
                '-DSEACASProj_ENABLE_ALL_PACKAGES:BOOL=OFF',
                '-DSEACASProj_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF',
                '-DSEACASProj_ENABLE_SECONDARY_TESTED_CODE:BOOL=OFF',
                '-DSEACASProj_ENABLE_SEACASIoss:BOOL=ON',
                '-DSEACASProj_ENABLE_SEACASExodus:BOOL=ON',
                '-DSEACASProj_ENABLE_SEACASExodus_for:BOOL=%s' % (
                    'ON' if '+fortran' in spec else 'OFF'),
                '-DSEACASProj_ENABLE_SEACASExoIIv2for32:BOOL=%s' % (
                    'ON' if '+fortran' in spec else 'OFF'),
            ])

            if '+applications' in spec:
                options.extend([
                    '-DSEACASProj_ENABLE_SEACASAprepro:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASAprepro_lib:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASConjoin:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASEjoin:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASEpu:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExo2mat:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExo_format:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExodiff:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASExplore:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASGrepos:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASMat2exo:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASNemslice:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASNemspread:BOOL=ON',
                ])

            if '+legacy' in spec:
                options.extend([
                    '-DSEACASProj_ENABLE_SEACASAlgebra:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASBlot:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASEx1ex2v2:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASEx2ex1v2:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASExomatlab:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASExotec2:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASExotxt:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASFastq:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASGen3D:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASGenshell:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASGjoin:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASMapvar:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASMapvar-kd:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASNemesis:BOOL=ON',
                    '-DSEACASProj_ENABLE_SEACASNumbers:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                    '-DSEACASProj_ENABLE_SEACASTxtexo:BOOL=%s' % (
                        'ON' if '+fortran' in spec else 'OFF'),
                ])

        # ##################### Dependencies ##########################
        # Always need NetCDF
        options.extend([
            '-DTPL_ENABLE_Netcdf:BOOL=ON',
            '-DNetCDF_ROOT:PATH=%s' % spec['netcdf'].prefix,
        ])

        if '+metis' in spec:
            options.extend([
                '-DTPL_ENABLE_METIS:BOOL=ON',
                '-DMETIS_LIBRARY_DIRS=%s' % spec['metis'].prefix.lib,
                '-DMETIS_LIBRARY_NAMES=metis',
                '-DTPL_METIS_INCLUDE_DIRS=%s' % spec['metis'].prefix.include,
                '-DTPL_ENABLE_ParMETIS:BOOL=ON',
                '-DParMETIS_LIBRARY_DIRS=%s;%s' % (
                    spec['parmetis'].prefix.lib, spec['metis'].prefix.lib),
                '-DParMETIS_LIBRARY_NAMES=parmetis;metis',
                '-DTPL_ParMETIS_INCLUDE_DIRS=%s;%s' % (
                    spec['parmetis'].prefix.include,
                    spec['metis'].prefix.include)
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_METIS:BOOL=OFF',
                '-DTPL_ENABLE_ParMETIS:BOOL=OFF',
            ])

        if '+matio' in spec:
            options.extend([
                '-DTPL_ENABLE_Matio:BOOL=ON',
                '-DMatio_ROOT:PATH=%s' % spec['matio'].prefix
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_Matio:BOOL=OFF'
            ])

        if '+cgns' in spec:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=ON',
                '-DCGNS_ROOT:PATH=%s' % spec['cgns'].prefix,
            ])
        else:
            options.extend([
                '-DTPL_ENABLE_CGNS:BOOL=OFF'
            ])

        # ################# RPath Handling ######################
        if sys.platform == 'darwin' and macos_version() >= Version('10.12'):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append('-DCMAKE_MACOSX_RPATH:BOOL=ON')
        else:
            options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s' %
                           self.prefix.lib)

        return options
