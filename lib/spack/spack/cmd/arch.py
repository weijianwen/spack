# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import spack.architecture as architecture

description = "print architecture information about this machine"
section = "system"
level = "short"


def setup_parser(subparser):
    parts = subparser.add_mutually_exclusive_group()
    parts.add_argument(
        '-p', '--platform', action='store_true', default=False,
        help='print only the platform')
    parts.add_argument(
        '-o', '--operating-system', action='store_true', default=False,
        help='print only the operating system')
    parts.add_argument(
        '-t', '--target', action='store_true', default=False,
        help='print only the target')


def arch(parser, args):
    arch = architecture.Arch(
        architecture.platform(), 'default_os', 'default_target')

    if args.platform:
        print(arch.platform)
    elif args.operating_system:
        print(arch.os)
    elif args.target:
        print(arch.target)
    else:
        print(arch)
