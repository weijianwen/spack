# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ruby(AutotoolsPackage):
    """A dynamic, open source programming language with a focus on
    simplicity and productivity."""

    homepage = "https://www.ruby-lang.org/"
    url      = "http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz"
    list_url = "http://cache.ruby-lang.org/pub/ruby/"
    list_depth = 1

    version('2.6.2', 'a0405d2bf2c2d2f332033b70dff354d224a864ab0edd462b7a413420453b49ab')
    version('2.5.3', '9828d03852c37c20fa333a0264f2490f07338576734d910ee3fd538c9520846c')
    version('2.2.0', 'cd03b28fd0b555970f5c4fd481700852')

    variant('openssl', default=True, description="Enable OpenSSL support")
    variant('readline', default=False, description="Enable Readline support")

    extendable = True

    depends_on('pkgconfig', type=('build'))
    depends_on('libffi')
    depends_on('zlib')
    depends_on('libx11')
    depends_on('tcl')
    depends_on('tk')
    depends_on('openssl@:1.0', when='@:2.3+openssl')
    depends_on('openssl', when='+openssl')
    depends_on('readline', when='+readline')

    # gcc-7-based build requires patches (cf. https://bugs.ruby-lang.org/issues/13150)
    patch('ruby_23_gcc7.patch', level=0, when='@2.2.0:2.2.999 %gcc@7:')
    patch('ruby_23_gcc7.patch', level=0, when='@2.3.0:2.3.4 %gcc@7:')
    patch('ruby_24_gcc7.patch', level=1, when='@2.4.0 %gcc@7:')

    resource(
        name='rubygems-updated-ssl-cert',
        url='https://raw.githubusercontent.com/rubygems/rubygems/master/lib/rubygems/ssl_certs/index.rubygems.org/GlobalSignRootCA.pem',
        sha256='df68841998b7fd098a9517fe971e97890be0fc93bbe1b2a1ef63ebdea3111c80',
        when='+openssl',
        destination='',
        placement='rubygems-updated-ssl-cert',
        expand=False
    )

    def url_for_version(self, version):
        url = "http://cache.ruby-lang.org/pub/ruby/{0}/ruby-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        args = []
        if '+openssl' in self.spec:
            args.append("--with-openssl-dir=%s" % self.spec['openssl'].prefix)
        if '+readline' in self.spec:
            args.append("--with-readline-dir=%s"
                        % self.spec['readline'].prefix)
        args.append('--with-tk=%s' % self.spec['tk'].prefix)
        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # TODO: do this only for actual extensions.
        # Set GEM_PATH to include dependent gem directories
        ruby_paths = []
        for d in dependent_spec.traverse():
            if d.package.extends(self.spec):
                ruby_paths.append(d.prefix)

        spack_env.set_path('GEM_PATH', ruby_paths)

        # The actual installation path for this gem
        spack_env.set('GEM_HOME', dependent_spec.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before ruby modules' install() methods.  Sets GEM_HOME
        and GEM_PATH to values appropriate for the package being built.

        In most cases, extensions will only need to have one line::

            gem('install', '<gem-name>.gem')
        """
        # Ruby extension builds have global ruby and gem functions
        module.ruby = Executable(join_path(self.spec.prefix.bin, 'ruby'))
        module.gem = Executable(join_path(self.spec.prefix.bin, 'gem'))

    @run_after('install')
    def post_install(self):
        """ RubyGems updated their SSL certificates at some point, so
        new certificates must be installed after Ruby is installed
        in order to download gems; see
        http://guides.rubygems.org/ssl-certificate-update/
        for details.
        """
        if self.spec.satisfies("+openssl"):
            rubygems_updated_cert_path = join_path(self.stage.source_path,
                                                   'rubygems-updated-ssl-cert',
                                                   'GlobalSignRootCA.pem')
            rubygems_certs_path = join_path(self.spec.prefix.lib,
                                            'ruby',
                                            '{0}.0'.format(self.spec.version.
                                                           up_to(2)),
                                            'rubygems',
                                            'ssl_certs')
            install(rubygems_updated_cert_path, rubygems_certs_path)
