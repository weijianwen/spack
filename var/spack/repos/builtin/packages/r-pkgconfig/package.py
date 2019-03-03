# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPkgconfig(RPackage):
    """Set configuration options on a per-package basis. Options set by a
     given package only apply to that package,
     other packages are unaffected."""

    homepage = "https://cran.rstudio.com/web/packages/pkgconfig/index.html"
    url      = "https://cran.rstudio.com/src/contrib/pkgconfig_2.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pkgconfig"

    version('2.0.2', sha256='25997754d1adbe7a251e3bf9879bb52dced27dd8b84767d558f0f644ca8d69ca')
    version('2.0.1', 'a20fd9588e37995995fa62dc4828002e')
