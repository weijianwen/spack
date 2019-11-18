# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Listres(AutotoolsPackage):
    """The listres program generates a list of X resources for a widget
    in an X client written using a toolkit based on libXt."""

    homepage = "http://cgit.freedesktop.org/xorg/app/listres"
    url      = "https://www.x.org/archive/individual/app/listres-1.0.3.tar.gz"

    version('1.0.3', sha256='87d5698b8aa4d841e45e6556932c9914210cbd8b10003d664b31185b087981be')

    depends_on('libxaw')
    depends_on('libxt')
    depends_on('libxmu')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
