# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Coreutils(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Core Utilities are the basic file, shell and text
       manipulation utilities of the GNU operating system.  These are
       the core utilities which are expected to exist on every
       operating system.
    """
    homepage = "http://www.gnu.org/software/coreutils/"
    gnu_mirror_path = "coreutils/coreutils-8.26.tar.xz"

    version('8.29', sha256='92d0fa1c311cacefa89853bdb53c62f4110cdfda3820346b59cbd098f40f955e')
    version('8.26', sha256='155e94d748f8e2bc327c66e0cbebdb8d6ab265d2f37c3c928f7bf6c3beba9a8e')
    version('8.23', sha256='ec43ca5bcfc62242accb46b7f121f6b684ee21ecd7d075059bf650ff9e37b82d')

    build_directory = 'spack-build'
