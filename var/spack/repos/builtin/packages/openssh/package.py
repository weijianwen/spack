# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openssh(AutotoolsPackage):
    """OpenSSH is the premier connectivity tool for remote login with the
       SSH protocol. It encrypts all traffic to eliminate
       eavesdropping, connection hijacking, and other attacks. In
       addition, OpenSSH provides a large suite of secure tunneling
       capabilities, several authentication methods, and sophisticated
       configuration options.
    """

    homepage = "https://www.openssh.com/"
    url      = "https://mirrors.sonic.net/pub/OpenBSD/OpenSSH/portable/openssh-7.6p1.tar.gz"

    version('8.3p1',   sha256='f2befbe0472fe7eb75d23340eb17531cb6b3aac24075e2066b41f814e12387b2')
    version('8.1p1',   sha256='02f5dbef3835d0753556f973cd57b4c19b6b1f6cd24c03445e23ac77ca1b93ff')
    version('7.9p1',   sha256='6b4b3ba2253d84ed3771c8050728d597c91cfce898713beb7b64a305b6f11aad')
    version('7.6p1',   sha256='a323caeeddfe145baaa0db16e98d784b1fbc7dd436a6bf1f479dfd5cd1d21723')
    version('7.5p1',   sha256='9846e3c5fab9f0547400b4d2c017992f914222b3fd1f8eee6c7dc6bc5e59f9f0')
    version('7.4p1',   sha256='1b1fc4a14e2024293181924ed24872e6f2e06293f3e8926a376b8aec481f19d1')
    version('7.3p1',   sha256='3ffb989a6dcaa69594c3b550d4855a5a2e1718ccdde7f5e36387b424220fbecc')
    version('7.2p2',   sha256='a72781d1a043876a224ff1b0032daa4094d87565a68528759c1c2cab5482548c')
    version('7.1p2',   sha256='dd75f024dcf21e06a0d6421d582690bf987a1f6323e32ad6619392f3bfde6bbd')
    version('7.0p1',   sha256='fd5932493a19f4c81153d812ee4e042b49bbd3b759ab3d9344abecc2bc1485e5')
    version('6.9p1',   sha256='6e074df538f357d440be6cf93dc581a21f22d39e236f217fcd8eacbb6c896cfe')
    version('6.8p1',   sha256='3ff64ce73ee124480b5bf767b9830d7d3c03bbcb6abe716b78f0192c37ce160e')
    version('6.7p1',   sha256='b2f8394eae858dabbdef7dac10b99aec00c95462753e80342e530bbb6f725507')
    version('6.6p1',   sha256='48c1f0664b4534875038004cc4f3555b8329c2a81c1df48db5c517800de203bb')

    depends_on('openssl@:1.0', when='@:7.7p1')
    depends_on('openssl')
    depends_on('libedit')
    depends_on('ncurses')
    depends_on('zlib')

    def configure_args(self):
        # OpenSSH's privilege separation path defaults to /var/empty. At
        # least newer versions want to create the directory during the
        # install step and fail if they cannot do so.
        args = ['--with-privsep-path={0}'.format(self.prefix.var.empty)]
        return args
