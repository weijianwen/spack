# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBh(RPackage):
    """Boost provides free peer-reviewed portable C++ source libraries. A large
    part of Boost is provided as C++ template code which is resolved entirely
    at compile-time without linking. This package aims to provide the most
    useful subset of Boost libraries for template use among CRAN package. By
    placing these libraries in this package, we offer a more efficient
    distribution system for CRAN as replication of this code in the sources of
    other packages is avoided. As of release 1.60.0-2, the following Boost
    libraries are included: 'algorithm' 'any' 'bimap' 'bind' 'circular_buffer'
    'concept' 'config' 'container' 'date'_'time' 'detail' 'dynamic_bitset'
    'exception' 'filesystem' 'flyweight' 'foreach' 'functional' 'fusion'
    'geometry' 'graph' 'heap' 'icl' 'integer' 'interprocess' 'intrusive' 'io'
    'iostreams' 'iterator' 'math' 'move' 'mpl' 'multiprcecision' 'numeric'
    'pending' 'phoenix' 'preprocessor' 'random' 'range' 'smart_ptr' 'spirit'
    'tuple' 'type_trains' 'typeof' 'unordered' 'utility' 'uuid'."""

    homepage = "https://cran.r-project.org/web/packages/BH/index.html"
    url      = "https://cran.r-project.org/src/contrib/BH_1.65.0-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/BH"

    version('1.69.0-1', sha256='a0fd4364b7e368f09c56dec030823f52c16da0787580af7e4615eddeb99baca2')
    version('1.65.0-1', '7d0402188e4af59f4103f36616d6ee55')
    version('1.60.0-2', 'b50fdc85285da05add4e9da664a2d551')
