# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Trimgalore(Package):
    """Trim Galore! is a wrapper around Cutadapt and FastQC to consistently
       apply adapter and quality trimming to FastQ files, with extra
       functionality for RRBS data."""

    homepage = "https://github.com/FelixKrueger/TrimGalore"
    url      = "https://github.com/FelixKrueger/TrimGalore/archive/0.4.4.tar.gz"

    version('0.6.1', sha256='658578c29d007fe66f9ab49608442be703a6fcf535db06eb82659c7edccb62b0')
    version('0.6.0', sha256='f374dfa4c94e2ad50c63276dda0f341fd95b29cb1d5a0e2ad56e8b0168b758ec')
    version('0.4.5', 'c71756042b2a65c34d483533a29dc206')
    version('0.4.4', 'aae1b807b48e38bae7074470203997bb')

    depends_on('perl', type=('build', 'run'))
    depends_on('py-cutadapt', type=('build', 'run'))
    depends_on('fastqc')

    def install(self, spec, prefix):
        filter_file(r'#!/usr/bin/perl', '#!/usr/bin/env perl', 'trim_galore')

        mkdirp(prefix.bin)
        install('trim_galore', prefix.bin)
