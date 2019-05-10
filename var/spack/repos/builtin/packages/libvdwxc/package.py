# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Libvdwxc(AutotoolsPackage):
    """Portable C library of density functionals with van der Waals
       interactions for density functional theory"""

    homepage = "https://libvdwxc.gitlab.io/libvdwxc/"
    url = "https://launchpad.net/libvdwxc/stable/0.4.0/+download/libvdwxc-0.4.0.tar.gz"

    version("0.4.0", "68196798d69d593b62ea9f482468db66")

    variant("mpi", default=True, description="Enable MPI support")
    variant("pfft", default=False, description="Enable support for PFFT")

    depends_on("fftw@3:", when="~mpi")
    depends_on("mpi@2:", when="+mpi")
    depends_on("fftw@3:+mpi", when="+mpi")
    depends_on("pfft", when="+pfft")

    # pfft needs MPI
    conflicts("~mpi", "+pfft")

    def configure_args(self):
        spec = self.spec

        args = [
            "--{0}-pfft".format(
                "with" if self.spec.satisfies("+pfft") else "without"
            ),
            "MPICC=",  # make sure both variables are always unset
            "MPIFC=",  # otherwise the configure scripts complains
        ]

        if spec.satisfies("+mpi"):
            # work around b0rken MPI detection: the MPI detection tests are
            # run with CC instead of MPICC, triggering an error. So, setting
            # CC/FC to the MPI compiler wrappers.
            args += [
                "--with-mpi",
                "CC={0}".format(spec["mpi"].mpicc),
                "FC={0}".format(spec["mpi"].mpifc),
            ]
        else:
            args += ["--without-mpi"]

        return args
