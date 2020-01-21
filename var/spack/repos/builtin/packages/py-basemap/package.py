# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "http://matplotlib.org/basemap/"

    version('1.2.0', sha256='bd5bf305918a2eb675939873b735238f9e3dfe6b5c290e37c41e5b082ff3639a')
    version('1.0.7', sha256='e07ec2e0d63b24c9aed25a09fe8aff2598f82a85da8db74190bac81cbf104531')

    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pyproj@:1.99', type=('build', 'run'))
    depends_on('py-pyshp', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('geos')

    def url_for_version(self, version):
        if version >= Version('1.2.0'):
            return 'https://github.com/matplotlib/basemap/archive/v{0}rel.tar.gz'.format(version)
        else:
            return 'https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-{0}/basemap-{0}.tar.gz'.format(version)

    def setup_build_environment(self, env):
        env.set('GEOS_DIR', self.spec['geos'].prefix)

    def install(self, spec, prefix):
        """Install everything from build directory."""
        args = self.install_args(spec, prefix)

        self.setup_py('install', *args)

        # namespace packages should not create an __init__.py file. This has
        # been reported to the basemap project in
        # https://github.com/matplotlib/basemap/issues/456
        for root, dirs, files in os.walk(spec.prefix.lib):
            for filename in files:
                if (filename == '__init__.py' and
                    os.path.basename(root) == 'mpl_toolkits'):
                    os.remove(os.path.join(root, filename))
