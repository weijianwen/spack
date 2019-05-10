# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XkeyboardConfig(AutotoolsPackage):
    """This project provides a consistent, well-structured, frequently
    released, open source database of keyboard configuration data. The
    project is targeted to XKB-based systems."""

    homepage = "https://www.freedesktop.org/wiki/Software/XKeyboardConfig/"
    url      = "https://www.x.org/archive/individual/data/xkeyboard-config/xkeyboard-config-2.18.tar.gz"

    version('2.18', '96c43e04dbfbb1e6e6abd4678292062c')

    depends_on('libx11@1.4.3:')

    depends_on('libxslt', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('intltool@0.30:', type='build')
    depends_on('xproto@7.0.20:', type='build')

    # TODO: missing dependencies
    # xgettext
    # msgmerge
    # msgfmt
    # gmsgfmt
    # perl@5.8.1:
    # perl XML::Parser

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('XKB_CONFIG_ROOT', self.prefix.share.X11.xkb)
        run_env.prepend_path('XKB_CONFIG_ROOT', self.prefix.share.X11.xkb)
