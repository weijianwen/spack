# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRasterio(PythonPackage):
    """Rasterio reads and writes geospatial raster data.
    Geographic information systems use GeoTIFF and other formats to
    organize and store gridded, or raster, datasets. Rasterio reads
    and writes these formats and provides a Python API based on N-D
    arrays."""

    homepage = "https://github.com/mapbox/rasterio"
    url      = "https://pypi.io/packages/source/r/rasterio/rasterio-1.0.24.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = ['rasterio', 'rasterio.rio']

    version('1.0.24', sha256='4839479621045211f66868ec49625979693450bc2e476f23e7e8ac4804eaf452')
    version('1.0a12', sha256='47d460326e04c64590ff56952271a184a6307f814efc34fb319c12e690585f3c')

    depends_on('python@3:', type=('build', 'run'), when='@1.1:')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-affine', type=('build', 'run'))
    depends_on('py-attrs', type=('build', 'run'))
    depends_on('py-click@4:7', type=('build', 'run'))
    depends_on('py-cligj@0.5:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-snuggs@1.4.1:', type=('build', 'run'))
    depends_on('py-click-plugins', type=('build', 'run'))
    depends_on('py-enum34', type='run', when='^python@:3.3')
    depends_on('gdal@1.11:')
    depends_on('jpeg')
    depends_on('py-pytest@2.8.2:', type='test')
    depends_on('py-boto3@1.2.4:', type='test')
    depends_on('py-packaging', type='test')
    depends_on('py-hypothesis', type='test')
    depends_on('py-futures', type='test', when='^python@:3.1')
    depends_on('py-mock', type='test', when='^python@:3.1')
