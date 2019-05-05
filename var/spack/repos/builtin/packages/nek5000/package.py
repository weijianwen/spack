# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os


class Nek5000(Package):
    """A fast and scalable high-order solver for computational fluid
       dynamics"""

    homepage = "https://nek5000.mcs.anl.gov/"
    url      = "https://github.com/Nek5000/Nek5000/releases/download/v17.0/Nek5000-v17.0.tar.gz"
    git      = "https://github.com/Nek5000/Nek5000.git"

    tags = ['cfd', 'flow', 'hpc', 'solver', 'navier-stokes',
            'spectral-elements', 'fluid', 'ecp', 'ecp-apps']

    version('develop', branch='master')
    version('17.0', '6a13bfad2ce023897010dd88f54a0a87')

    # MPI, Profiling and Visit variants
    variant('mpi',       default=True, description='Build with MPI.')
    variant('profiling', default=True, description='Build with profiling data.')
    variant('visit',     default=False, description='Build with Visit.')

    # TODO: add a variant 'blas' or 'external-blas' to enable the usage of
    #       Spack installed/configured blas.

    # Dependencies
    depends_on('mpi', when="+mpi")

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.f77:
            msg = 'Cannot build Nek5000 without a Fortran 77 compiler.'
            raise RuntimeError(msg)

    @run_after('install')
    def test_install(self):
        with working_dir('short_tests/eddy'):
            os.system(join_path(self.prefix.bin, 'makenek') + ' eddy_uv')
            if not os.path.isfile(join_path(os.getcwd(), 'nek5000')):
                msg = 'Cannot build example: short_tests/eddy.'
                raise RuntimeError(msg)

    def install(self, spec, prefix):
        bin_dir     = 'bin'

        # Do not use the Spack compiler wrappers.
        # Use directly the compilers:
        fc  = self.compiler.f77
        cc  = self.compiler.cc

        fflags = spec.compiler_flags['fflags']
        cflags = spec.compiler_flags['cflags']

        if self.compiler.name in ['xl', 'xl_r']:
            # Use '-qextname' to add underscores.
            # Use '-WF,-qnotrigraph' to fix an error about a string: '... ??'
            fflags += ['-qextname', '-WF,-qnotrigraph']

        error = Executable(fc)('empty.f', output=str, error=str,
                               fail_on_error=False)

        if 'gfortran' in error or 'GNU' in error or 'gfortran' in fc:
            # Use '-std=legacy' to suppress an error that used to be a
            # warning in previous versions of gfortran.
            fflags += ['-std=legacy']

        fflags = ' '.join(fflags)
        cflags = ' '.join(cflags)

        with working_dir(bin_dir):
            if '+mpi' in spec:
                fc  = spec['mpi'].mpif77
                cc  = spec['mpi'].mpicc
            else:
                filter_file(r'^#MPI=0', 'MPI=0', 'makenek')

            if '+profiling' not in spec:
                filter_file(r'^#PROFILING=0', 'PROFILING=0', 'makenek')

            if '+visit' in spec:
                filter_file(r'^#VISIT=1', 'VISIT=1', 'makenek')
                filter_file(r'^#VISIT_INSTALL=.*', 'VISIT_INSTALL=\"' +
                            spec['visit'].prefix.bin + '\"', 'makenek')

            # Update the makenek to use correct compilers and
            # Nek5000 source.
            filter_file(r'^#FC\s*=.*', 'FC="{0}"'.format(fc), 'makenek')
            filter_file(r'^#CC\s*=.*', 'CC="{0}"'.format(cc), 'makenek')
            filter_file(r'^#SOURCE_ROOT\s*=\"\$H.*',  'SOURCE_ROOT=\"' +
                        prefix.bin.Nek5000 + '\"',  'makenek')
            if fflags:
                filter_file(r'^#FFLAGS=.*', 'FFLAGS+=" {0}"'.format(fflags),
                            'makenek')
            if cflags:
                filter_file(r'^#CFLAGS=.*', 'CFLAGS+=" {0}"'.format(cflags),
                            'makenek')

        with working_dir('core'):
            if self.compiler.name in ['xl', 'xl_r']:
                # Patch 'core/makenek.inc' and 'makefile.template' to use
                # '-qextname' when checking for underscore becasue 'xl'/'xl_r'
                # use this option to enable the addition of the underscore.
                filter_file(r'^\$FCcomp -c ', '$FCcomp -qextname -c ',
                            'makenek.inc')
                filter_file(r'\$\(FC\) -c \$\(L0\)',
                            '$(FC) -c -qextname $(L0)', 'makefile.template')

        # Install Nek5000/bin in prefix/bin
        install_tree(bin_dir, prefix.bin)

        # Copy Nek5000 source to prefix/bin
        install_tree('../Nek5000', prefix.bin.Nek5000)
