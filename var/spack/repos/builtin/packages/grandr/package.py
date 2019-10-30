# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Grandr(AutotoolsPackage):
    """RandR user interface using GTK+ libraries."""

    homepage = "https://cgit.freedesktop.org/xorg/app/grandr"
    url      = "https://www.x.org/archive/individual/app/grandr-0.1.tar.gz"

    version('0.1', sha256='67a049c8dccdb48897efbd86c2b1d3b0ff5ce3c7859c46b0297d64c881b36d24')

    depends_on('gtkplus@2.0.0:')
    depends_on('gconf')
    depends_on('xrandr@1.2:')
