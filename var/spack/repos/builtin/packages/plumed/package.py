# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os.path


class Plumed(AutotoolsPackage):
    """PLUMED is an open source library for free energy calculations in
    molecular systems which works together with some of the most popular
    molecular dynamics engines.

    Free energy calculations can be performed as a function of many order
    parameters with a particular focus on biological problems, using state
    of the art methods such as metadynamics, umbrella sampling and
    Jarzynski-equation based steered MD.

    The software, written in C++, can be easily interfaced with both fortran
    and C/C++ codes.
    """
    homepage = 'http://www.plumed.org/'
    url = 'https://github.com/plumed/plumed2/archive/v2.5.0.tar.gz'

    version('2.5.0', 'd1277d86a4aa766bfe97513d7969bfb7')
    version('2.4.4', 'e8ef700fb4740b177cf660313c9805e6')
    version('2.4.2', '0f66f24b4c763ae8b2f39574113e9935')
    version('2.4.1', '6558e1fd02fc46e847ab6a3fb5ed5411')
    version('2.3.5', '3cc5f025cb6f5d963f3c778f15c77d44')
    version('2.3.3', '9f5729e406e79a06a16976fcb020e024')
    version('2.3.0', 'a9b5728f115dca8f0519111f1f5a6fa5')
    version('2.2.4', 'afb00da25a3fbd47acf377e53342059d')
    version('2.2.3', 'a6e3863e40aac07eb8cf739cbd14ecf8')

    # Variants. PLUMED by default builds a number of optional modules.
    # The ones listed here are not built by default for various reasons,
    # such as stability, lack of testing, or lack of demand.
    # FIXME: This needs to be an optional
    variant(
        'optional_modules',
        default='all',
        values=lambda x: True,
        description='String that is used to build optional modules'
    )
    variant('shared', default=True, description='Builds shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('gsl', default=True, description='Activates GSL support')

    # Dependencies. LAPACK and BLAS are recommended but not essential.
    depends_on('zlib')
    depends_on('blas')
    depends_on('lapack')
    # For libmatheval support through the 'function' module
    # which is enabled by default (or when optional_modules=all)
    depends_on('libmatheval')

    depends_on('mpi', when='+mpi')
    depends_on('gsl', when='+gsl')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    force_autoreconf = True

    parallel = False

    def apply_patch(self, other):

        # The name of MD engines differ slightly from the ones used in Spack
        format_strings = collections.defaultdict(
            lambda: '{0.name}-{0.version}'
        )
        format_strings['espresso'] = 'q{0.name}-{0.version}'
        format_strings['amber'] = '{0.name}{0.version}'

        get_md = lambda x: format_strings[x.name].format(x)

        # Get available patches
        plumed_patch = Executable(
            os.path.join(self.spec.prefix.bin, 'plumed-patch')
        )

        out = plumed_patch('-q', '-l', output=str)
        available = out.split(':')[-1].split()

        # Check that `other` is among the patchable applications
        if get_md(other) not in available:
            msg = '{0.name}@{0.version} is not among the MD engine'
            msg += ' that can be patched by {1.name}@{1.version}.\n'
            msg += 'Supported engines are:\n'
            for x in available:
                msg += x + '\n'
            raise RuntimeError(msg.format(other, self.spec))

        # Call plumed-patch to patch executables
        target = format_strings[other.name].format(other)
        plumed_patch('-p', '-e', target)

    def setup_dependent_package(self, module, dependent_spec):
        # Make plumed visible from dependent packages
        module.plumed = dependent_spec['plumed'].command

    @property
    def plumed_inc(self):
        return os.path.join(
            self.prefix.lib, 'plumed', 'src', 'lib', 'Plumed.inc'
        )

    @run_before('autoreconf')
    def filter_gslcblas(self):
        # This part is needed to avoid linking with gsl cblas
        # interface which will mask the cblas interface
        # provided by optimized libraries due to linking order
        filter_file('-lgslcblas', '', 'configure.ac')

    def configure_args(self):
        spec = self.spec

        # From plumed docs :
        # Also consider that this is different with respect to what some other
        # configure script does in that variables such as MPICXX are
        # completely ignored here. In case you work on a machine where CXX is
        # set to a serial compiler and MPICXX to a MPI compiler, to compile
        # with MPI you should use:
        #
        # > ./configure CXX="$MPICXX"

        # The configure.ac script may detect the wrong linker for
        # LD_RO which causes issues at link time. Here we work around
        # the issue saying we have no LD_RO executable.
        configure_opts = ['--disable-ld-r']

        # If using MPI then ensure the correct compiler wrapper is used.
        if '+mpi' in spec:
            configure_opts.extend([
                '--enable-mpi',
                'CXX={0}'.format(spec['mpi'].mpicxx)
            ])

            # If the MPI dependency is provided by the intel-mpi package then
            # the following additional argument is required to allow it to
            # build.
            if 'intel-mpi' in spec:
                configure_opts.extend([
                    'STATIC_LIBS=-mt_mpi'
                ])

        # Set flags to help find gsl
        if '+gsl' in self.spec:
            gsl_libs = self.spec['gsl'].libs
            blas_libs = self.spec['blas'].libs
            configure_opts.append('LDFLAGS={0}'.format(
                (gsl_libs + blas_libs).ld_flags
            ))

        # Additional arguments
        configure_opts.extend([
            '--enable-shared={0}'.format('yes' if '+shared' in spec else 'no'),
            '--enable-gsl={0}'.format('yes' if '+gsl' in spec else 'no')
        ])

        # Construct list of optional modules

        # If we have specified any optional modules then add the argument to
        # enable or disable them.
        optional_modules = self.spec.variants['optional_modules'].value
        if optional_modules:
            # From 'configure --help' @2.3:
            # all/none/reset or : separated list such as
            # +crystallization:-bias default: reset
            configure_opts.append(
                '--enable-modules={0}'.format(optional_modules)
            )

        return configure_opts
