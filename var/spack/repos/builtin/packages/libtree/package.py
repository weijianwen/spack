# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtree(CMakePackage):
    """ldd as a tree with an option to bundle dependencies into a
       single folder"""

    homepage = "https://github.com/haampie/libtree"
    url      = "https://github.com/haampie/libtree/releases/download/v1.0.3/sources.tar.gz"

    maintainers = ['haampie']

    version('1.1.2', sha256='31641c6bf6c2980ffa7b4c57392460434f97ba66fe51fe6346867430b33a0374')
    version('1.1.1', sha256='3e8543145a40a94e9e2ce9fed003d2bf68294e1fce9607028a286bc132e17dc4')
    version('1.1.0', sha256='6cf36fb9a4c8c3af01855527d4931110732bb2d1c19be9334c689f1fd1c78536')
    version('1.0.4', sha256='b15a54b6f388b8bd8636e288fcb581029f1e65353660387b0096a554ad8e9e45')
    version('1.0.3', sha256='67ce886c191d50959a5727246cdb04af38872cd811c9ed4e3822f77a8f40b20b')
