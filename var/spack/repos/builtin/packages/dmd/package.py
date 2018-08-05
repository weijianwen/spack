##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import shutil
import glob


class Dmd(MakefilePackage):
    """DMD is the reference compiler for the D programming language."""

    homepage = "https://github.com/dlang/dmd"
    url      = "https://github.com/dlang/dmd/archive/v2.081.1.tar.gz"

    version('2.081.1', sha256='14f3aafe1c93c86646aaeb3ed7361a5fc5a24374cf25c8848c81942bfd9fae1a')

    depends_on('openssl')
    depends_on('curl')

    # https://wiki.dlang.org/Building_under_Posix
    resource(name='druntime',
             url='https://github.com/dlang/druntime/archive/v2.081.1.tar.gz',
             md5='49c8ba48fcb1e53d553a52d8ed7f9164',
             placement='druntime')
    resource(name='phobos',
             url='https://github.com/dlang/phobos/archive/v2.081.1.tar.gz',
             md5='ccf4787275b490eb2ddfc6713f9e9882',
             placement='phobos')
    resource(name='tools',
             url='https://github.com/dlang/tools/archive/v2.081.1.tar.gz',
             md5='a3bc7ed3d60b39712ef011bf19b3d427',
             placement='tools')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.linux.bin64)

    def do_stage(self, mirror_only=False):
        # wrap (decorate) the standard expand_archive step with a
        # helper, then call the real do_stage().
        self.stage.expand_archive = self.unpack_dmd(self.stage.expand_archive)
        super(Dmd, self).do_stage(mirror_only)

    def unpack_dmd(self, f):
        def wrap():
            f() # call the original expand_archive()
            with working_dir(self.stage.path):
                dir_dmd = glob.glob(join_path('dmd*'))[0]
                # mkdir = which('mkdir')
                # mkdir('dmd')
                # mv =  which('mv')
                # mv(join_path(dir_dmd, '*'), 'dmd')
                # shutil.move(join_path(dir_dmd, '*'), 'dmd')
        return wrap

    def edit(self, spec, prefix):
        makefile = FileFilter('dmd/posix.mak')
        makefile.filter('$(PWD)/../install', prefix, string=True)

    def build(self, spec, prefix):
        with working_dir('dmd'):
            make('-f', 'posix.mak', 'AUTO_BOOTSTRAP=1')
        with working_dir('phobos'):
            make('-f', 'posix.mak')

    def install(self, spec, prefix):
        with working_dir('dmd'):
            make('-f', 'posix.mak', 'install', 'AUTO_BOOTSTRAP=1')
