# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from llnl.util.filesystem import working_dir
from spack.directives import depends_on, extends
from spack.package import PackageBase, run_after


class SIPPackage(PackageBase):
    """Specialized class for packages that are built using the
    SIP build system. See https://www.riverbankcomputing.com/software/sip/intro
    for more information.

    This class provides the following phases that can be overridden:

    * configure
    * build
    * install

    The configure phase already adds a set of default flags. To see more
    options, run ``python configure.py --help``.
    """
    # Default phases
    phases = ['configure', 'build', 'install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'SIPPackage'

    #: Callback names for install-time test
    install_time_test_callbacks = ['import_module_test']

    extends('python')

    depends_on('qt')
    depends_on('py-sip')

    def configure_file(self):
        """Returns the name of the configure file to use."""
        return 'configure.py'

    def python(self, *args, **kwargs):
        """The python ``Executable``."""
        inspect.getmodule(self).python(*args, **kwargs)

    def configure(self, spec, prefix):
        """Configure the package."""
        configure = self.configure_file()

        args = self.configure_args()

        args.extend([
            '--verbose',
            '--confirm-license',
            '--qmake', spec['qt'].prefix.bin.qmake,
            '--sip', spec['py-sip'].prefix.bin.sip,
            '--sip-incdir', os.path.join(
                spec['py-sip'].prefix,
                spec['python'].package.python_include_dir
            ),
            '--bindir', prefix.bin,
            '--destdir', inspect.getmodule(self).site_packages_dir,
        ])

        self.python(configure, *args)

    def configure_args(self):
        """Arguments to pass to configure."""
        return []

    def build(self, spec, prefix):
        """Build the package."""
        args = self.build_args()

        inspect.getmodule(self).make(*args)

    def build_args(self):
        """Arguments to pass to build."""
        return []

    def install(self, spec, prefix):
        """Install the package."""
        args = self.install_args()

        inspect.getmodule(self).make('install', parallel=False, *args)

    def install_args(self):
        """Arguments to pass to install."""
        return []

    # Testing

    def import_module_test(self):
        """Attempts to import the module that was just installed.

        This test is only run if the package overrides
        :py:attr:`import_modules` with a list of module names."""

        # Make sure we are importing the installed modules,
        # not the ones in the current directory
        with working_dir('spack-test', create=True):
            for module in self.import_modules:
                self.python('-c', 'import {0}'.format(module))

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
