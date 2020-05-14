# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Draco(CMakePackage):
    """Draco is an object-oriented component library geared towards numerically
    intensive, radiation (particle) transport applications built for parallel
    computing hardware. It consists of semi-independent packages and a robust
    build system. """

    homepage = "https://github.com/lanl/draco"
    url = "https://github.com/lanl/Draco/archive/draco-7_1_0.zip"
    git = "https://github.com/lanl/Draco.git"
    maintainers = ['KineticTheory']

    version('develop', branch='develop')
    version('7.6.0',  sha256='c2c6b329620d7bcb0f2fc14371f105dfb80a84e7c5adbb34620777034b15c7c9')
    version('7.5.0',  sha256='0bb12b5f5ff60ba3087310c07da42e8d4f481ec4259daaa24ec240815a2e9dec')
    version('7.4.0',  sha256='61da2c3feace0e92c5410c9e9e613708fdf8954b1367cdc62c415329b0ddab6e')
    version('7.3.0',  sha256='dc47ef6c1e04769ea177a10fc6ddf506f3e1e8d36eb5d49f4bc38cc509e24f10')
    version('7.2.0',  sha256='ac4eac03703d4b7344fa2390a54140533c5e1f6ea0d59ef1f1d525c434ebe639')
    version('7.1.0',  sha256='eca6bb86eb930837fb5e09b76c85c200b2c1522267cc66f81f2ec11a8262b5c9')
    version('6.25.0', sha256='e27eba44f397e7d111ff9a45b518b186940f75facfc6f318d76bd0e72f987440')
    version('6.23.0', sha256='edf20308746c06647087cb4e6ae7656fd057a89091a22bcba8f17a52e28b7849')
    version('6.22.0', sha256='4d1ed54944450c4ec7d00d7ba371469506c6985922f48f780bae2580c9335b86')
    version('6.21.0', sha256='f1ac88041606cdb1dfddd3bc74db0f1e15d8fc9d0a1eed939c8aa0fa63a85b55')
    version('6.20.1', sha256='b1c51000c9557e0818014713fce70d681869c50ed9c4548dcfb2e9219c354ebe')
    version('6.20.0', sha256='a6e3142c1c90b09c4ff8057bfee974369b815122b01d1f7b57888dcb9b1128f6')

    variant('build_type', default='Release', description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('eospac',   default=True, description='Enable EOSPAC support')
    variant('lapack',   default=True, description='Enable LAPACK wrapper')
    variant('libquo',   default=True, description='Enable Quo wrapper')
    variant('parmetis', default=True, description='Enable Parmetis support')
    variant('qt',       default=False, description='Enable Qt support')
    variant('superlu_dist', default=True, description='Enable SuperLU-DIST support')

    depends_on('gsl')
    depends_on('mpi@3:',      type=('build', 'link', 'run'))
    depends_on('numdiff',     type='build')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('random123',   type='build')

    depends_on('cmake@3.9:',  when='@:6.99',        type='build')
    depends_on('cmake@3.11:', when='@7.0.0:7.1.99', type='build')
    depends_on('cmake@3.14:', when='@7.2:',         type='build')
    depends_on('eospac@6.3:', when='+eospac')
    depends_on('lapack',      when='+lapack')
    depends_on('libquo',      when='@7.4.0:+libquo')
    depends_on('metis',       when='+parmetis')
    depends_on('parmetis',    when='+parmetis')
    depends_on('qt',          when='+qt',
               type=('build', 'link', 'run'))
    depends_on('superlu-dist@:5.99', when='+superlu_dist')

    # Fix python discovery.
    patch('d710.patch', when='@7.1.0^python@3:')
    patch('d710-python2.patch', when='@7.1.0^python@2.7:2.99')
    patch('d730.patch', when='@7.3.0:7.3.99')
    patch('d740.patch', when='@7.4.0:7.4.99')

    def url_for_version(self, version):
        url = "https://github.com/lanl/Draco/archive/draco-{0}.zip"
        return url.format(version.underscored)

    def cmake_args(self):
        options = []
        options.extend([
            '-Wno-dev',
            '-DBUILD_TESTING={0}'.format('ON' if self.run_tests else 'OFF')
        ])
        return options
