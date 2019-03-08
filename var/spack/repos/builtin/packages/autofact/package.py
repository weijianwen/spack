# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Autofact(Package):
    """An Automatic Functional Annotation and Classification Tool"""

    homepage = "http://megasun.bch.umontreal.ca/Software/AutoFACT.htm"
    url      = "http://megasun.bch.umontreal.ca/Software/AutoFACT_v3_4.tar"

    version('3_4', sha256='1465d263b19adb42f01f6e636ac40ef1c2e3dbd63461f977b89da9493fe9c6f4')

    depends_on('perl', type='run')
    depends_on('perl-bio-perl', type='run')
    depends_on('perl-io-string', type='run')
    depends_on('perl-lwp', type='run')
    depends_on('blast-legacy', type='run')

    def patch(self):
        with working_dir('scripts'):
            files = glob.iglob("*.pl")
            for file in files:
                change = FileFilter(file)
                change.filter('usr/bin/perl', 'usr/bin/env perl')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.scripts)
        run_env.set('PATH2AUTOFACT', self.prefix)
