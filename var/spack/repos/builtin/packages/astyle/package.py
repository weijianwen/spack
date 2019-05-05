# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Astyle(MakefilePackage):
    """A Free, Fast, and Small Automatic Formatter for C, C++, C++/CLI,
    Objective-C, C#, and Java Source Code.
    """

    homepage = "http://astyle.sourceforge.net/"
    url = "https://sourceforge.net/projects/astyle/files/astyle/astyle%203.0.1/astyle_3.0.1_linux.tar.gz"
    # Gentoo alternative
    # url = "http://distfiles.gentoo.org/distfiles/astyle_3.0.1_linux.tar.gz"

    version('3.1',    '7712622f62661b1d8cb1062d7fedc390')
    version('3.0.1',  'c301f09679efa2e1eb6e6b5fd33788b4')
    version('2.06',   'ff588e7fcede824591cf5b9085df109d')
    version('2.05.1', '4142d178047d7040da3e0e2f1b030a1a')
    version('2.04',   '30b1193a758b0909d06e7ee8dd9627f6')

    parallel = False

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, 'build', self.compiler.name)

    def edit(self, spec, prefix):
        makefile = join_path(self.build_directory, 'Makefile')
        filter_file(r'^CXX\s*=.*', 'CXX=%s' % spack_cxx, makefile)
        # strangely enough install -o $(USER) -g $(USER) stoped working on OSX
        if sys.platform == 'darwin':
            filter_file(r'^INSTALL=.*', 'INSTALL=install', makefile)

    @property
    def install_targets(self):
        return ['install', 'prefix={0}'.format(self.prefix)]
