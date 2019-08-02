# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

# Although this looks like an Autotools package, it's not one. Refer to:
# https://github.com/flame/blis/issues/17
# https://github.com/flame/blis/issues/195
# https://github.com/flame/blis/issues/197


class Blis(Package):
    """BLIS is a portable software framework for instantiating high-performance
    BLAS-like dense linear algebra libraries. The framework was designed to
    isolate essential kernels of computation that, when optimized, immediately
    enable optimized implementations of most of its commonly used and
    computationally intensive operations. BLIS is written in ISO C99 and
    available under a new/modified/3-clause BSD license. While BLIS exports a
    new BLAS-like API, it also includes a BLAS compatibility layer which gives
    application developers access to BLIS implementations via traditional BLAS
    routine calls. An object-based API unique to BLIS is also available."""

    homepage = "https://github.com/flame/blis"
    url      = "https://github.com/flame/blis/archive/0.4.0.tar.gz"
    git      = "https://github.com/flame/blis.git"

    version('master', branch='master')
    version('0.6.0', sha256='ad5765cc3f492d0c663f494850dafc4d72f901c332eb442f404814ff2995e5a9')
    version('0.5.0', sha256='1a004d69c139e8a0448c6a6007863af3a8c3551b8d9b8b73fe08e8009f165fa8')
    version('0.4.0', sha256='9c7efd75365a833614c01b5adfba93210f869d92e7649e0b5d9edc93fc20ea76')
    version('0.3.2', sha256='b87e42c73a06107d647a890cbf12855925777dc7124b0c7698b90c5effa7f58f')
    version('0.3.1', sha256='957f28d47c5cf71ffc62ce8cc1277e17e44d305b1c2fa8506b0b55617a9f28e4')
    version('0.3.0', sha256='d34d17df7bdc2be8771fe0b7f867109fd10437ac91e2a29000a4a23164c7f0da')
    version('0.2.2', sha256='4a7ecb56034fb20e9d1d8b16e2ef587abbc3d30cb728e70629ca7e795a7998e8')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'openmp', 'none'),
        multi=False
    )

    variant(
        'blas', default=True,
        description='BLAS compatibility',
    )

    variant(
        'cblas', default=False,
        description='CBLAS compatibility',
    )

    variant(
        'shared', default=True,
        description='Build shared library',
    )

    variant(
        'static', default=True,
        description='Build static library',
    )

    # TODO: add cpu variants. Currently using auto.
    # If one knl, should the default be memkind ?

    # BLIS has it's own API but can be made compatible with BLAS
    # enabling CBLAS automatically enables BLAS.

    provides('blas', when="+blas")
    provides('blas', when="+cblas")

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        config_args = []

        config_args.append("--enable-threading=" +
                           spec.variants['threads'].value)

        if '+cblas' in spec:
            config_args.append("--enable-cblas")
        else:
            config_args.append("--disable-cblas")

        if '+blas' in spec:
            config_args.append("--enable-blas")
        else:
            config_args.append("--disable-blas")

        if '+shared' in spec:
            config_args.append("--enable-shared")
        else:
            config_args.append("--disable-shared")

        if '+static' in spec:
            config_args.append("--enable-static")
        else:
            config_args.append("--disable-static")

        # FIXME: add cpu isa variants.
        config_args.append("auto")

        configure("--prefix=" + prefix,
                  *config_args)

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        make('check')

    def install(self, spec, prefix):
        make('install')
