# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Binutils(AutotoolsPackage, GNUMirrorPackage):
    """GNU binutils, which contain the linker, assembler, objdump and others"""

    homepage = "http://www.gnu.org/software/binutils/"
    gnu_mirror_path = "binutils/binutils-2.28.tar.bz2"

    version('2.32', sha256='de38b15c902eb2725eac6af21183a5f34ea4634cb0bcef19612b50e5ed31072d')
    version('2.31.1', sha256='ffcc382695bf947da6135e7436b8ed52d991cf270db897190f19d6f9838564d0')
    version('2.29.1', sha256='1509dff41369fb70aed23682351b663b56db894034773e6dbf7d5d6071fc55cc')
    version('2.28', sha256='6297433ee120b11b4b0a1c8f3512d7d73501753142ab9e2daa13c5a3edd32a72')
    version('2.27', sha256='369737ce51587f92466041a97ab7d2358c6d9e1b6490b3940eb09fb0a9a6ac88')
    version('2.26', sha256='c2ace41809542f5237afc7e3b8f32bb92bc7bc53c6232a84463c423b0714ecd9')
    version('2.25.1', sha256='b5b14added7d78a8d1ca70b5cb75fef57ce2197264f4f5835326b0df22ac9f22')
    version('2.25', sha256='22defc65cfa3ef2a3395faaea75d6331c6e62ea5dfacfed3e2ec17b08c882923')
    version('2.24', sha256='e5e8c5be9664e7f7f96e0d09919110ab5ad597794f5b1809871177a0f0f14137')
    version('2.23.2', sha256='fe914e56fed7a9ec2eb45274b1f2e14b0d8b4f41906a5194eac6883cfe5c1097')
    version('2.20.1', sha256='71d37c96451333c5c0b84b170169fdcb138bbb27397dc06281905d9717c8ed64')

    variant('plugins', default=False,
            description="enable plugins, needed for gold linker")
    variant('gold', default=True, description="build the gold linker")
    variant('libiberty', default=False, description='Also install libiberty.')
    variant('nls', default=True, description='Enable Native Language Support')
    variant('headers', default=False, description='Install extra headers (e.g. ELF)')

    patch('cr16.patch', when='@:2.29.1')
    patch('update_symbol-2.26.patch', when='@2.26')

    depends_on('zlib')
    depends_on('gettext', when='+nls')

    # Prior to 2.30, gold did not distribute the generated files and
    # thus needs bison, even for a one-time build.
    depends_on('m4', type='build', when='@:2.29.99 +gold')
    depends_on('bison', type='build', when='@:2.29.99 +gold')

    def configure_args(self):
        spec = self.spec

        configure_args = [
            '--disable-dependency-tracking',
            '--disable-werror',
            '--enable-multilib',
            '--enable-shared',
            '--enable-64-bit-bfd',
            '--enable-targets=all',
            '--with-system-zlib',
            '--with-sysroot=/',
        ]

        if '+gold' in spec:
            configure_args.append('--enable-gold')

        if '+plugins' in spec:
            configure_args.append('--enable-plugins')

        if '+libiberty' in spec:
            configure_args.append('--enable-install-libiberty')

        if '+nls' in spec:
            configure_args.append('--enable-nls')
            configure_args.append('LDFLAGS=-lintl')
        else:
            configure_args.append('--disable-nls')

        # To avoid namespace collisions with Darwin/BSD system tools,
        # prefix executables with "g", e.g., gar, gnm; see Homebrew
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/binutils.rb
        if spec.satisfies('platform=darwin'):
            configure_args.append('--program-prefix=g')

        return configure_args

    @run_after('install')
    def install_headers(self):
        # some packages (like TAU) need the ELF headers, so install them
        # as a subdirectory in include/extras
        if '+headers' in self.spec:
            extradir = join_path(self.prefix.include, 'extra')
            mkdirp(extradir)
            # grab the full binutils set of headers
            install_tree('include', extradir)
            # also grab the headers from the bfd directory
            for current_file in glob.glob(join_path(self.build_directory,
                                                    'bfd', '*.h')):
                install(current_file, extradir)

    def flag_handler(self, name, flags):
        # To ignore the errors of narrowing conversions for
        # the Fujitsu compiler
        if name == 'cxxflags'\
           and (self.compiler.name == 'fj' or self.compiler.name == 'clang')\
           and self.version <= ver('2.31.1'):
            flags.append('-Wno-narrowing')
        return (flags, None, None)
