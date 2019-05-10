# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Dyninst(CMakePackage):
    """API for dynamic binary instrumentation.  Modify programs while they
    are executing without recompiling, re-linking, or re-executing."""

    homepage = "https://paradyn.org"
    git      = "https://github.com/dyninst/dyninst.git"

    version('develop', branch='master')
    version('10.0.0', tag='v10.0.0')
    version('9.3.2', tag='v9.3.2')
    version('9.3.0', tag='v9.3.0')
    version('9.2.0', tag='v9.2.0')
    version('9.1.0', tag='v9.1.0')
    version('8.2.1', tag='v8.2.1')

    variant('openmp', default=True,
            description='Enable OpenMP support for ParseAPI '
            '(version 10.0.0 or later)')

    variant('static', default=False,
            description='Build static libraries')

    variant('stat_dysect', default=False,
            description="Patch for STAT's DySectAPI")

    boost_libs = '+atomic+chrono+date_time+filesystem+system+thread+timer'

    depends_on('boost@1.61.0:1.69.99' + boost_libs)
    depends_on('libiberty+pic')

    # Dyninst uses elf@1 (elfutils) starting with 9.3.0, and used
    # elf@0 (libelf) before that.
    depends_on('elf@1', type='link', when='@9.3.0:')
    depends_on('elf@0', type='link', when='@:9.2.99')

    # Dyninst uses libdw from elfutils (same elf@1) starting with
    # 10.x, and used libdwarf before that.
    depends_on('libdwarf', when='@:9.99')

    depends_on('tbb@2018.6:', when='@10.0:')

    depends_on('cmake@3.4.0:', type='build', when='@10.0:')
    depends_on('cmake@2.8:', type='build', when='@:9.99')

    patch('stat_dysect.patch', when='+stat_dysect')
    patch('stackanalysis_h.patch', when='@9.2.0')
    patch('v9.3.2-auto.patch', when='@9.3.2 %gcc@:4.7.99')
    patch('tribool.patch', when='@9.3.0:10.0.0 ^boost@1.69:')

    # Versions 9.3.x used cotire, but have no knob to turn it off.
    # Cotire has no real use for one-time builds and can break
    # parallel builds with both static and shared libs.
    @when('@9.3.0:9.3.99')
    def patch(self):
        filter_file('USE_COTIRE true', 'USE_COTIRE false',
                    'cmake/shared.cmake')

    def cmake_args(self):
        spec = self.spec

        # Elf -- the directory containing libelf.h.
        elf = spec['elf'].prefix
        elf_include = os.path.dirname(
            find_headers('libelf', elf.include, recursive=True)[0])

        # Dwarf -- the directory containing elfutils/libdw.h or
        # libdwarf.h, and the path to libdw.so or libdwarf.so.
        if spec.satisfies('@10.0.0:'):
            dwarf_include = elf.include
            dwarf_lib = find_libraries('libdw', elf, recursive=True)
        else:
            dwarf_include = spec['libdwarf'].prefix.include
            dwarf_lib = spec['libdwarf'].libs

        args = [
            '-DPATH_BOOST=%s' % spec['boost'].prefix,
            '-DIBERTY_LIBRARIES=%s' % spec['libiberty'].libs,
        ]

        # 10.1 changed the spelling of LibElf and LibDwarf.
        if spec.satisfies('@10.1.0:'):
            args.extend([
                '-DLibElf_INCLUDE_DIR=%s' % elf_include,
                '-DLibElf_LIBRARIES=%s' % spec['elf'].libs,
                '-DLibDwarf_INCLUDE_DIR=%s' % dwarf_include,
                '-DLibDwarf_LIBRARIES=%s' % dwarf_lib,
            ])
        else:
            args.extend([
                '-DLIBELF_INCLUDE_DIR=%s' % elf_include,
                '-DLIBELF_LIBRARIES=%s' % spec['elf'].libs,
                '-DLIBDWARF_INCLUDE_DIR=%s' % dwarf_include,
                '-DLIBDWARF_LIBRARIES=%s' % dwarf_lib,
            ])

        # TBB include and lib directories, version 10.x or later.
        if spec.satisfies('@10.0.0:'):
            args.extend([
                '-DTBB_INCLUDE_DIRS=%s' % spec['tbb'].prefix.include,
                '-DTBB_LIBRARY=%s' % spec['tbb'].prefix.lib,
            ])

        # Openmp applies to version 10.x or later.
        if spec.satisfies('@10.0.0:'):
            if '+openmp' in spec:
                args.append('-DUSE_OpenMP=ON')
            else:
                args.append('-DUSE_OpenMP=OFF')

        # Static libs started with version 9.1.0.
        if spec.satisfies('@9.1.0:'):
            if '+static' in spec:
                args.append('-DENABLE_STATIC_LIBS=1')
            else:
                args.append('-DENABLE_STATIC_LIBS=NO')

        return args
