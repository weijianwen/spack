# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class Wireshark(CMakePackage):
    """Graphical network analyzer and capture tool"""

    homepage = "https://www.wireshark.org"
    url      = "https://www.wireshark.org/download/src/all-versions/wireshark-2.6.0.tar.xz"

    version('2.6.0', sha256='711c7f01d27a8817d58277a5487cef3e3c7bab1c8caaf8f4c92aa21015b9117f')

    variant('libssh',   default=False, description='Build with libssh')
    variant('nghttp2',  default=False, description='Build with nghttp2')
    variant('qt',       default=False, description='Build with qt')
    variant('headers',  default=True, description='Install headers')

    depends_on('bison',     type='build')
    depends_on('c-ares')
    depends_on('doxygen',   type='build')
    depends_on('flex',      type='build')
    depends_on('git',       type='build')
    depends_on('glib')
    depends_on('gnutls')
    depends_on('libgcrypt@1.4.2:')
    depends_on('libmaxminddb')
    depends_on('libtool@2.2.2:', type='build')
    depends_on('libpcap')
    depends_on('lua@5.0.0:5.2.99')
    depends_on('krb5')
    depends_on('pkgconfig', type='build')
    depends_on('libssh',    when='+libssh')
    depends_on('nghttp2',   when='+nghttp2')
    depends_on('qt@4.8:',   when='+qt')

    def cmake_args(self):
        args = [
            '-DENEABLE_CARES=ON',
            '-DENABLE_GNUTLS=ON',
            '-DENABLE_LUA=ON',
            '-DENABLE_MAXMINDDB=ON',
            '-DYACC_EXECUTABLE=' + self.spec['bison'].prefix.bin.yacc,
            '-DGIT_EXECUTABLE=' + self.spec['git'].prefix.bin.git,
            '-DPCAP_INCLUDE_DIR=' + self.spec['libpcap'].prefix.include,
            '-DPCAP_LIB=' + str(self.spec['libpcap'].libs),
            '-DLUA_INCLUDE_DIR=' + self.spec['lua'].prefix.include,
            '-DLUA_LIBRARY=' + str(self.spec['lua'].libs),
            '-DBUILD_wireshark_gtk=OFF',
            '-DENABLE_PORTAUDIO=OFF',
            '-DENABLE_GTK3=OFF',
            '-DBUILD_SMI=OFF',
        ]

        if self.spec.satisfies('+qt'):
            args.append('-DBUILD_wireshark=ON')
            args.append('-DENABLE_APPLICATION_BUNDLE=ON')
            if self.spec['qt'].version >= Version(5):
                args.append('-DENABLE_QT5=ON')
            else:
                args.append('-DENABLE_QT5=OFF')
        else:
            args.append('-DBUILD_wireshark=OFF')
            args.append('-DENABLE_APPLICATION_BUNDLE=OFF')
            args.append('-DENABLE_QT5=OFF')

        if self.spec.satisfies('+libssh'):
            args.append('-DBUILD_sshdump=ON')
            args.append('-DBUILD_ciscodump=ON')
        else:
            args.append('-DBUILD_sshdump=OFF')
            args.append('-DBUILD_ciscodump=OFF')

        if self.spec.satisfies('+nghttp2'):
            args.append('-DBUILD_NGHTTP2=ON')
        else:
            args.append('-DBUILD_NGHTTP2=OFF')

        return args

    @run_after('install')
    def symlink(self):
        if self.spec.satisfies('platform=darwin'):
            link(join_path(self.prefix,
                           'Wireshark.app/Contents/MacOS/Wireshark'),
                 self.prefix.bin.wireshark)

    @run_after('install')
    def install_headers(self):
        if self.spec.satisfies('+headers'):
            folders = ['.', 'epan/crypt', 'epan/dfilter', 'epan/dissectors',
                       'epan/ftypes', 'epan/wmem', 'wiretap', 'wsutil']
            for folder in folders:
                headers = glob.glob(join_path(folder, '*.h'))
                for h in headers:
                    install(h, join_path(prefix.include, 'wireshark', folder))
