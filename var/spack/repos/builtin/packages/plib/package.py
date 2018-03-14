##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install plib
#
# You can edit this file again by typing:
#
#     spack edit plib
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Plib(AutotoolsPackage):
    """PLIB is a suite of portable game libraries."""

    homepage = "http://plib.sourceforge.net"
    url      = "http://plib.sourceforge.net/dist/plib-1.8.5.tar.gz"

    version('1.8.5', '47a6fbf63668c1eed631024038b2ea90')

    variant('X', default=False, description='Enable X support')

    depends_on('libx11', when='+X')
    depends_on('mesa', when='+X')

    def configure_args(self):
        spec = self.spec
        args = []
        if '+X' in spec:
            args.extend(['--with-x',
                         '--with-GL={0}'.format(spec['mesa'].prefix)])
        else:
            args.extend(['--without-x',
                         '--without-GL'])
        return args
