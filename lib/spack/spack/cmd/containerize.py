# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import spack.container

description = ("creates recipes to build images for different"
               " container runtimes")
section = "container"
level = "long"


def containerize(parser, args):
    config_dir = args.env_dir or os.getcwd()
    config_file = os.path.abspath(os.path.join(config_dir, 'spack.yaml'))
    if not os.path.exists(config_file):
        msg = 'file not found: {0}'
        raise ValueError(msg.format(config_file))

    config = spack.container.validate(config_file)

    recipe = spack.container.recipe(config)
    print(recipe)
