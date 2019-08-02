# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class CbtfArgonavisGui(QMakePackage):
    """CBTF Argo Navis GUI project contains the GUI that views OpenSpeedShop
       performance information by loading in the Sqlite database files.
    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"
    git      = "https://github.com/OpenSpeedShop/cbtf-argonavis-gui.git"

    version('develop', branch='master')
    version('1.3.0.0', branch='1.3.0.0')

    depends_on("cmake@3.0.2:", type='build')

    depends_on('qt@5.10.0:')

    depends_on("boost@1.66.0:1.69.0")

    # For MRNet
    depends_on("mrnet@5.0.1-3:+lwthreads", when='@develop')
    depends_on("mrnet@5.0.1-3+lwthreads", when='@1.3.0.0:9999')

    # Dependencies for the openspeedshop cbtf packages.
    depends_on("cbtf@develop", when='@develop')
    depends_on("cbtf@1.9.1.0:9999", when='@1.3.0.0:9999')

    depends_on("cbtf-krell@develop", when='@develop')
    depends_on("cbtf-krell@1.9.1.0:9999", when='@1.3.0.0:9999')

    depends_on("cbtf-argonavis@develop", when='@develop')
    depends_on("cbtf-argonavis@1.9.1.0:9999", when='@1.3.0.0:9999')

    depends_on("cuda")

    depends_on("openspeedshop-utils+cuda@develop", when='@develop')
    depends_on("openspeedshop-utils@2.3.1.3:+cuda", when='@1.3.0.0:9999')

    # For Xerces-C
    depends_on("xerces-c")

    depends_on("graphviz@2.40.1:", when='@develop')
    depends_on("graphviz@2.40.1", when='@1.3.0.0:9999')

    depends_on("qtgraph")

    parallel = False

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""
        spack_env.set('BOOSTROOT', self.spec['boost'].prefix)
        spack_env.set('CBTF_ROOT', self.spec['cbtf'].prefix)
        spack_env.set('CBTF_KRELL_ROOT', self.spec['cbtf-krell'].prefix)
        spack_env.set('CBTF_ARGONAVIS_ROOT',
                      self.spec['cbtf-argonavis'].prefix)
        spack_env.set('OSS_CBTF_ROOT', self.spec['openspeedshop-utils'].prefix)
        spack_env.set('GRAPHVIZ_ROOT', self.spec['graphviz'].prefix)
        spack_env.set('QTGRAPHLIB_ROOT', self.spec['qtgraph'].prefix)
        spack_env.set('KRELL_ROOT_MRNET', self.spec['mrnet'].prefix)
        spack_env.set('KRELL_ROOT_XERCES', self.spec['xerces-c'].prefix)
        spack_env.set('INSTALL_ROOT', self.spec.prefix)

        # The implementor of qtgraph has set up the library and include
        # paths in a non-conventional way.  We reflect that here.
        # What library suffix should be used based on library existence
        if os.path.isdir(self.spec['qtgraph'].prefix.lib64):
            qtgraph_lib_dir = self.spec['qtgraph'].prefix.lib64
        else:
            qtgraph_lib_dir = self.spec['qtgraph'].prefix.lib

        run_env.prepend_path(
            'LD_LIBRARY_PATH', join_path(
                qtgraph_lib_dir,
                '{0}'.format(self.spec['qt'].version.up_to(3))))

        # The openspeedshop libraries are needed to actually load the
        # performance information into the GUI.
        run_env.prepend_path(
            'LD_LIBRARY_PATH', self.spec['openspeedshop-utils'].prefix.lib64)

    def qmake_args(self):
        options = ['-o', 'Makefile', 'openss-gui.pro']
        return options
