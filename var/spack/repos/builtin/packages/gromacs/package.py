# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gromacs(CMakePackage):
    """GROMACS (GROningen MAchine for Chemical Simulations) is a molecular
    dynamics package primarily designed for simulations of proteins, lipids
    and nucleic acids. It was originally developed in the Biophysical
    Chemistry department of University of Groningen, and is now maintained
    by contributors in universities and research centers across the world.

    GROMACS is one of the fastest and most popular software packages
    available and can run on CPUs as well as GPUs. It is free, open source
    released under the GNU General Public License. Starting from version 4.6,
    GROMACS is released under the GNU Lesser General Public License.
    """

    homepage = 'http://www.gromacs.org'
    url      = 'http://ftp.gromacs.org/gromacs/gromacs-5.1.2.tar.gz'
    git      = 'https://github.com/gromacs/gromacs.git'
    maintainers = ['junghans', 'marvinbernhardt']

    version('develop', branch='master')
    version('2019.2', sha256='bcbf5cc071926bc67baa5be6fb04f0986a2b107e1573e15fadcb7d7fc4fb9f7e')
    version('2019.1', sha256='b2c37ed2fcd0e64c4efcabdc8ee581143986527192e6e647a197c76d9c4583ec')
    version('2019', sha256='c5b281a5f0b5b4eeb1f4c7d4dc72f96985b566561ca28acc9c7c16f6ee110d0b')
    version('2018.4', sha256='6f2ee458c730994a8549d6b4f601ecfc9432731462f8bd4ffa35d330d9aaa891')
    version('2018.3', sha256='4423a49224972969c52af7b1f151579cea6ab52148d8d7cbae28c183520aa291')
    version('2018.2', sha256='4bdde8120c510b6543afb4b18f82551fddb11851f7edbd814aa24022c5d37857')
    version('2018.1', sha256='4d3533340499323fece83b4a2d4251fa856376f2426c541e00b8e6b4c0d705cd')
    version('2018',   sha256='deb5d0b749a52a0c6083367b5f50a99e08003208d81954fb49e7009e1b1fd0e9')
    version('2016.5', sha256='57db26c6d9af84710a1e0c47a1f5bf63a22641456448dcd2eeb556ebd14e0b7c')
    version('2016.4', sha256='4be9d3bfda0bdf3b5c53041e0b8344f7d22b75128759d9bfa9442fe65c289264')
    version('2016.3', sha256='7bf00e74a9d38b7cef9356141d20e4ba9387289cbbfd4d11be479ef932d77d27')
    version('5.1.5',  sha256='c25266abf07690ecad16ed3996899b1d489cbb1ef733a1befb3b5c75c91a703e')
    version('5.1.4',  sha256='0f3793d8f1f0be747cf9ebb0b588fb2b2b5dc5acc32c3046a7bee2d2c03437bc')
    version('5.1.2',  sha256='39d6f1d7ae8ba38cea6089da40676bfa4049a49903d21551abc030992a58f304')
    version('4.5.5', sha256='e0605e4810b0d552a8761fef5540c545beeaf85893f4a6e21df9905a33f871ba')

    variant('mpi', default=True, description='Activate MPI support')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant(
        'double', default=False,
        description='Produces a double precision version of the executables')
    variant('plumed', default=False, description='Enable PLUMED support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel',
                    'Reference', 'RelWithAssert', 'Profile'))
    variant('simd', default='auto',
            description='The SIMD instruction set to use',
            values=('auto', 'none', 'SSE2', 'SSE4.1', 'AVX_128_FMA', 'AVX_256',
                    'AVX2_128', 'AVX2_256', 'AVX_512', 'AVX_512_KNL',
                    'IBM_QPX', 'Sparc64_HPC_ACE', 'IBM_VMX', 'IBM_VSX',
                    'ARM_NEON', 'ARM_NEON_ASIMD'))
    variant('rdtscp', default=True, description='Enable RDTSCP instruction usage')
    variant('mdrun_only', default=False,
            description='Enables the build of a cut-down version'
            ' of libgromacs and/or the mdrun program')
    variant('openmp', default=True, description='Enables OpenMP at configure time')
    variant('double_precision', default=False, description='Enables a double-precision configuration')

    depends_on('mpi', when='+mpi')
    depends_on('plumed+mpi', when='+plumed+mpi')
    depends_on('plumed~mpi', when='+plumed~mpi')
    depends_on('fftw')
    depends_on('cmake@2.8.8:3.99.99', type='build')
    depends_on('cmake@3.4.3:3.99.99', type='build', when='@2018:')
    depends_on('cuda', when='+cuda')

    patch('gmxDetectCpu-cmake-3.14.patch', when='@2018:^cmake@3.14.0:')
    patch('gmxDetectSimd-cmake-3.14.patch', when='@:2017.99^cmake@3.14.0:')

    def patch(self):
        if '+plumed' in self.spec:
            self.spec['plumed'].package.apply_patch(self)

    def cmake_args(self):

        options = []

        if '+mpi' in self.spec:
            options.append('-DGMX_MPI:BOOL=ON')

        if '+double' in self.spec:
            options.append('-DGMX_DOUBLE:BOOL=ON')

        if '~shared' in self.spec:
            options.append('-DBUILD_SHARED_LIBS:BOOL=OFF')

        if '+cuda' in self.spec:
            options.append('-DGMX_GPU:BOOL=ON')
            options.append('-DCUDA_TOOLKIT_ROOT_DIR:STRING=' +
                           self.spec['cuda'].prefix)
        else:
            options.append('-DGMX_GPU:BOOL=OFF')

        simd_value = self.spec.variants['simd'].value
        if simd_value == 'auto':
            pass
        elif simd_value == 'none':
            options.append('-DGMX_SIMD:STRING=None')
        else:
            options.append('-DGMX_SIMD:STRING=' + simd_value)

        if '-rdtscp' in self.spec:
            options.append('-DGMX_USE_RDTSCP:BOOL=OFF')
        else:
            options.append('-DGMX_USE_RDTSCP:BOOL=ON')

        if '+mdrun_only' in self.spec:
            options.append('-DGMX_BUILD_MDRUN_ONLY:BOOL=ON')
        else:
            options.append('-DGMX_BUILD_MDRUN_ONLY:BOOL=OFF')

        if '~openmp' in self.spec:
            options.append('-DGMX_OPENMP:BOOL=OFF')
        else:
            options.append('-DGMX_OPENMP:BOOL=ON')

        if '+double_precision' in self.spec:
            options.append('-DGMX_RELAXED_DOUBLE_PRECISION:BOOL=ON')
        else:
            options.append('-DGMX_RELAXED_DOUBLE_PRECISION:BOOL=OFF')

        return options
