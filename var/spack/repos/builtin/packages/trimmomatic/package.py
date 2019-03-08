# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Trimmomatic(Package):
    """A flexible read trimming tool for Illumina NGS data."""

    homepage = "http://www.usadellab.org/cms/?page=trimmomatic"
    url      = "http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-0.36.zip"

    # Older version aren't explicitly made available, but the URL
    # works as we'd like it to, so...
    version('0.38', sha256='d428af42b6c400a2e7ee5e6b4cab490eddc621f949b086bd7dddb698dcf1647c')
    version('0.36', '8549130d86b6f0382b1a71a2eb45de39')
    version('0.33', '924fc8eb38fdff71740a0e05d32d6a2b')

    depends_on('java@8', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'trimmomatic-{v}.jar'.format(v=self.version.dotted)
        install(jar_file, prefix.bin)

        # Put the adapter files someplace sensible
        install_tree('adapters', prefix.share.adapters)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "trimmomatic.sh")
        script = prefix.bin.trimmomatic
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('trimmomatic.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
