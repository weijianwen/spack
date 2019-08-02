# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys


class Graphviz(AutotoolsPackage):
    """Graph Visualization Software"""

    homepage = 'http://www.graphviz.org'
    git      = 'https://gitlab.com/graphviz/graphviz.git'

    # This commit hash is tag='stable_release_2.40.1'
    version('2.40.1', commit='67cd2e5121379a38e0801cc05cce5033f8a2a609')

    # We try to leave language bindings enabled if they don't cause
    # build issues or add dependencies.
    variant('sharp', default=False,
            description='Enable for optional sharp language bindings'
            ' (not yet functional)')
    variant('go', default=False,
            description='Enable for optional go language bindings'
            ' (not yet functional)')
    variant('guile', default=False,
            description='Enable for optional guile language bindings'
            ' (not yet functional)')
    variant('io', default=False,
            description='Enable for optional io language bindings'
            ' (not yet functional)')
    variant('java', default=False,  # Spack has no Java support
            description='Enable for optional java language bindings')
    variant('lua', default=False,
            description='Enable for optional lua language bindings'
            ' (not yet functional)')
    variant('ocaml', default=False,
            description='Enable for optional ocaml language bindings'
            ' (not yet functional)')
    variant('perl', default=False,    # Spack has no Perl support
            description='Enable for optional perl language bindings')
    variant('php', default=False,
            description='Enable for optional php language bindings'
            ' (not yet functional)')
    variant('python', default=False,    # Build issues with Python 2/3
            description='Enable for optional python language bindings'
            ' (not yet functional)')
    variant('r', default=False,
            description='Enable for optional r language bindings'
            ' (not yet functional)')
    variant('ruby', default=False,
            description='Enable for optional ruby language bindings'
            ' (not yet functional)')
    variant('tcl', default=False,
            description='Enable for optional tcl language bindings'
            ' (not yet functional)')

    variant('pangocairo', default=False,
            description='Build with pango+cairo support (more output formats)')
    variant('libgd', default=False,
            description='Build with libgd support (more output formats)')
    variant('gts', default=False,
            description='Build with GNU Triangulated Surface Library')
    variant('expat', default=False,
            description='Build with Expat support (enables HTML-like labels)')
    variant('ghostscript', default=False,
            description='Build with Ghostscript support')
    variant('qt', default=False,
            description='Build with Qt support')
    variant('gtkplus', default=False,
            description='Build with GTK+ support')

    patch('http://www.linuxfromscratch.org/patches/blfs/svn/graphviz-2.40.1-qt5-1.patch',
          sha256='bd532df325df811713e311d17aaeac3f5d6075ea4fd0eae8d989391e6afba930',
          when='+qt^qt@5:')
    patch('https://raw.githubusercontent.com/easybuilders/easybuild-easyconfigs/master/easybuild/easyconfigs/g/Graphviz/Graphviz-2.38.0_icc_sfio.patch',
          sha256='393a0a772315a89dcc970b5efd4765d22dba83493d7956303673eb89c45b949f',
          level=0,
          when='%intel')
    patch('https://raw.githubusercontent.com/easybuilders/easybuild-easyconfigs/master/easybuild/easyconfigs/g/Graphviz/Graphviz-2.40.1_icc_vmalloc.patch',
          sha256='813e6529e79161a18b0f24a969b7de22f8417b2e942239e658b5402884541bc2',
          when='%intel')

    parallel = False

    # These language bindings have been tested, we know they work.
    tested_bindings = ('+java', )

    # These language bindings have not yet been tested.  They
    # likely need additional dependencies to get working.
    untested_bindings = (
        '+perl',
        '+sharp', '+go', '+guile', '+io',
        '+lua', '+ocaml', '+php',
        '+python', '+r', '+ruby', '+tcl')

    for b in tested_bindings + untested_bindings:
        depends_on('swig', type='build', when=b)

    depends_on('java', when='+java')
    depends_on('python@2:2.8', when='+python')

    # +pangocairo
    depends_on('cairo', when='+pangocairo')
    depends_on('pango', when='+pangocairo')
    depends_on('freetype', when='+pangocairo')
    depends_on('glib', when='+pangocairo')
    depends_on('fontconfig', when='+pangocairo')
    depends_on('libpng', when='+pangocairo')
    depends_on('zlib', when='+pangocairo')
    # +libgd
    depends_on('libgd', when='+libgd')
    depends_on('fontconfig', when='+libgd')
    depends_on('freetype', when='+libgd')
    # +gts
    depends_on('gts', when='+gts')
    # +expat
    depends_on('expat', when='+expat')
    # +ghostscript
    depends_on('ghostscript', when='+ghostscript')
    # +qt
    depends_on('qt', when='+qt')
    # +gtkplus
    depends_on('gtkplus', when='+gtkplus')

    # Build dependencies
    depends_on('pkgconfig', type='build')
    # The following are needed when building from git
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('libtool', type='build')

    def autoreconf(self, spec, prefix):
        # We need to generate 'configure' when checking out sources from git
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        # Else bootstrap (disabling auto-configure with NOCONFIG)
        bash = which('bash')
        bash('./autogen.sh', 'NOCONFIG')

    def configure_args(self):
        spec = self.spec
        options = []

        need_swig = False

        for var in self.untested_bindings:
            if var in spec:
                raise InstallError(
                    "The variant {0} for language bindings has not been "
                    "tested.  It might or might not work.  To try it "
                    "out, run `spack edit graphviz`, and then move '{0}' "
                    "from the `untested_bindings` list to the "
                    "`tested_bindings` list.  Be prepared to add "
                    "required dependencies.  "
                    "Please then submit a pull request to "
                    "http://github.com/spack/spack".format(var))
            options.append('--disable-%s' % var[1:])

        for var in self.tested_bindings:
            if var in spec:
                need_swig = True
                options.append('--enable-{0}'.format(var[1:]))
            else:
                options.append('--disable-{0}'.format(var[1:]))

        if need_swig:
            options.append('--enable-swig=yes')
        else:
            options.append('--enable-swig=no')

        for var in ('+pangocairo', '+libgd', '+gts', '+expat', '+ghostscript',
                    '+qt', '+gtkplus'):
            feature = var[1:]
            if feature == 'gtkplus':
                # In spack terms, 'gtk+' is 'gtkplus' while
                # the relative configure option is 'gtk'
                feature = 'gtk'
            if var in spec:
                options.append('--with-{0}'.format(feature))
            else:
                options.append('--without-{0}'.format(feature))

        # On OSX fix the compiler error:
        # In file included from tkStubLib.c:15:
        # /usr/include/tk.h:78:11: fatal error: 'X11/Xlib.h' file not found
        #       include <X11/Xlib.h>
        if sys.platform == 'darwin':
            options.append('CFLAGS=-I/opt/X11/include')

        return options
