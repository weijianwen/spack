# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Opencv(CMakePackage):
    """OpenCV is released under a BSD license and hence it's free for both
    academic and commercial use. It has C++, C, Python and Java interfaces and
    supports Windows, Linux, Mac OS, iOS and Android. OpenCV was designed for
    computational efficiency and with a strong focus on real-time applications.
    Written in optimized C/C++, the library can take advantage of multi-core
    processing. Enabled with OpenCL, it can take advantage of the hardware
    acceleration of the underlying heterogeneous compute platform. Adopted all
    around the world, OpenCV has more than 47 thousand people of user community
    and estimated number of downloads exceeding 9 million. Usage ranges from
    interactive art, to mines inspection, stitching maps on the web or through
    advanced robotics.
    """

    homepage = 'http://opencv.org/'
    url      = 'https://github.com/Itseez/opencv/archive/3.1.0.tar.gz'
    git      = 'https://github.com/opencv/opencv.git'

    version('master', branch='master')
    version('4.1.0-openvino', sha256='58764d2487c6fb4cd950fb46483696ae7ae28e257223d6e44e162caa22ee9e5c')
    version('4.1.0',          sha256='8f6e4ab393d81d72caae6e78bd0fd6956117ec9f006fba55fcdb88caf62989b7', preferred=True)
    version('4.0.1-openvino', sha256='8cbe32d12a70decad7a8327eb4fba46016a9c47ff3ba6e114d27b450f020716f')
    version('4.0.1',          sha256='7b86a0ee804244e0c407321f895b15e4a7162e9c5c0d2efc85f1cadec4011af4')
    version('4.0.0-openvino', sha256='aa910078ed0b7e17bd10067e04995c131584a6ed6d0dcc9ca44a292aa8e296fc')
    version('4.0.0',          sha256='3787b3cc7b21bba1441819cb00c636911a846c0392ddf6211d398040a1e4886c')
    version('3.4.6',          sha256='e7d311ff97f376b8ee85112e2b536dbf4bdf1233673500175ed7cf21a0089f6d')
    version('3.4.5',          sha256='0c57d9dd6d30cbffe68a09b03f4bebe773ee44dc8ff5cd6eaeb7f4d5ef3b428e')
    version('3.4.4',          sha256='a35b00a71d77b484f73ec485c65fe56c7a6fa48acd5ce55c197aef2e13c78746')
    version('3.4.3',    '712896f5815938c014c199dde142d508')
    version('3.4.1',    'a0b7a47899e67b3490ea31edc4f6e8e6')
    version('3.4.0',    '170732dc760e5f7ddeccbe53ba5d16a6')
    version('3.3.1',    'b1ed9aea030bb5bd9df28524d97de84c')
    version('3.3.0',    '98a4e4c6f23ec725e808a891dc11eec4')
    version('3.2.0',    '1ea44a1d98c126ad40079d8eb914a72e')
    version('3.1.0',    'a0669e22172dfc3225835b180744c9f0')
    version('2.4.13.2', 'fe52791ce523681a67036def4c25261b')
    version('2.4.13.1', 'f6d354500d5013e60dc0fc44b07a63d1')
    version('2.4.13',   '8feb45a71adad89b8017a777477c3eff')
    version('2.4.12.3', '2496a4a4caf8fecfbfc294fbe6a814b0')
    version('2.4.12.2', 'bc0c60c2ea1cf4078deef99569912fc7')
    version('2.4.12.1', '7192f51434710904b5e3594872b897c3')

    # Standard variants
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant('lapack', default=True, description='Include Lapack library support')
    variant('powerpc', default=False, description='Enable PowerPC for GCC')
    variant('vsx', default=False, description='Enable POWER8 and above VSX (64-bit little-endian)')
    variant('fast-math', default=False,
            description='Enable -ffast-math (not recommended for GCC 4.6.x)')

    # OpenCV modules
    variant('calib3d', default=True, description='calib3d module')
    variant('core', default=True, description='Include opencv_core module into the OpenCV build')
    variant('dnn', default=True, description='Build DNN support')
    variant('features2d', default=True, description='features2d module')
    variant('flann', default=True, description='flann module')
    variant('highgui', default=True, description='Include opencv_highgui module into the OpenCV build')
    variant('imgproc', default=True, description='Include opencv_imgproc module into the OpenCV build')
    variant('java', default=True,
            description='Activates support for Java')
    variant('ml', default=True, description='Build ML support')
    variant('python', default=True,
            description='Enables the build of Python extensions')
    variant('stitching', default=True, description='stitching module')
    variant('superres', default=True, description='superres module')
    variant('ts', default=True, description='Include opencv_ts module into the OpenCV build')
    variant('video', default=True, description='video module')
    variant('videostab', default=True, description='videostab module')
    variant('videoio', default=True, description='videoio module')

    # Optional 3rd party components
    variant('cuda', default=True, description='Activates support for CUDA')
    # Cuda@10.0.130 does not support gcc > 7
    conflicts('%gcc@7:', when='+cuda')
    variant('eigen', default=True, description='Activates support for eigen')
    variant('ipp', default=True, description='Activates support for IPP')
    variant('ipp_iw', default=True, description='Build IPP IW from source')
    variant('jasper', default=True, description='Activates support for JasPer')
    variant('jpeg', default=True, description='Include JPEG support')
    variant('opencl', default=True, description='Include OpenCL Runtime support')
    variant('opencl_svm', default=True, description='Include OpenCL Shared Virtual Memory support')
    variant('openclamdfft', default=True, description='Include OpenCL AMD OpenCL FFT library support')
    variant('openclamdblas', default=True, description='Include OpenCL AMD OpenCL BLAS library support')
    variant('openmp', default=True, description='Activates support for OpenMP threads')
    variant('pthreads_pf', default=True, description='Use pthreads-based parallel_for')
    variant('png', default=True, description='Include PNG support')
    variant('qt', default=False, description='Activates support for QT')
    variant('gtk', default=True, description='Activates support for GTK')
    variant('tiff', default=True, description='Include TIFF support')
    variant('vtk', default=True, description='Activates support for VTK')
    variant('zlib', default=True, description='Build zlib from source')

    # Patch to fix conflict between CUDA and OpenCV (reproduced with 3.3.0
    # and 3.4.1) header file that have the same name.Problem is fixed in
    # the current development branch of OpenCV. See #8461 for more information.
    patch('dnn_cuda.patch', when='@3.3.0:3.4.1+cuda+dnn')

    depends_on('eigen~mpfr', when='+eigen', type='build')

    depends_on('zlib', when='+zlib')
    depends_on('libpng', when='+png')
    depends_on('jpeg', when='+jpeg')
    depends_on('libtiff', when='+tiff')

    depends_on('jasper', when='+jasper')
    depends_on('cuda', when='+cuda')
    depends_on('gtkplus', when='+gtk')
    depends_on('vtk', when='+vtk')
    depends_on('qt', when='+qt')
    depends_on('java', when='+java')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('protobuf@3.5.0', when='@3.4.1: +dnn')
    depends_on('protobuf@3.1.0', when='@3.3.0:3.4.0 +dnn')

    depends_on('ffmpeg', when='+videoio')
    depends_on('mpi', when='+videoio')

    extends('python', when='+python')

    def cmake_args(self):
        spec = self.spec

        # Standard variants
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format((
                'ON' if '+shared' in spec else 'OFF')),
            '-DENABLE_PRECOMPILED_HEADERS:BOOL=OFF',
            '-DWITH_LAPACK={0}'.format((
                'ON' if '+lapack' in spec else 'OFF')),
            '-DENABLE_POWERPC={0}'.format((
                'ON' if '+powerpc' in spec else 'OFF')),
            '-DENABLE_VSX={0}'.format((
                'ON' if '+vsx' in spec else 'OFF')),
            '-DENABLE_FAST_MATH={0}'.format((
                'ON' if '+fast-math' in spec else 'OFF')),
        ]

        # modules
        args.extend([
            '-DBUILD_opencv_calib3d={0}'.format((
                'ON' if '+calib3d' in spec else 'OFF')),
            '-DBUILD_opencv_core:BOOL={0}'.format((
                'ON' if '+core' in spec else 'OFF')),
            '-DBUILD_opencv_dnn:BOOL={0}'.format((
                'ON' if '+dnn' in spec else 'OFF')),
            '-DBUILD_opencv_features2d={0}'.format((
                'ON' if '+features2d' in spec else 'OFF')),
            '-DBUILD_opencv_flann={0}'.format((
                'ON' if '+flann' in spec else 'OFF')),
            '-DBUILD_opencv_highgui:BOOL={0}'.format((
                'ON' if '+highgui' in spec else 'OFF')),
            '-DBUILD_opencv_imgproc:BOOL={0}'.format((
                'ON' if '+imgproc' in spec else 'OFF')),
            '-DBUILD_opencv_java:BOOL={0}'.format((
                'ON' if '+java' in spec else 'OFF')),
            '-DBUILD_opencv_ml={0}'.format((
                'ON' if '+ml' in spec else 'OFF')),
            '-DBUILD_opencv_stitching={0}'.format((
                'ON' if '+stitching' in spec else 'OFF')),
            '-DBUILD_opencv_superres={0}'.format((
                'ON' if '+superres' in spec else 'OFF')),
            '-DBUILD_opencv_ts={0}'.format((
                'ON' if '+ts' in spec else 'OFF')),
            '-DBUILD_opencv_video={0}'.format((
                'ON' if '+video' in spec else 'OFF')),
            '-DBUILD_opencv_videostab={0}'.format((
                'ON' if '+videostab' in spec else 'OFF')),
            '-DBUILD_opencv_videoio={0}'.format((
                'ON' if '+videoio' in spec else 'OFF')),
        ])

        # 3rd party components
        args.extend([
            '-DBUILD_IPP_IW:BOOL={0}'.format((
                'ON' if '+ipp_iw' in spec else 'OFF')),
            '-DWITH_CUDA:BOOL={0}'.format((
                'ON' if '+cuda' in spec else 'OFF')),
            '-DWITH_EIGEN:BOOL={0}'.format((
                'ON' if '+eigen' in spec else 'OFF')),
            '-DWITH_IPP:BOOL={0}'.format((
                'ON' if '+ipp' in spec else 'OFF')),
            '-DWITH_JASPER:BOOL={0}'.format((
                'ON' if '+jasper' in spec else 'OFF')),
            '-DWITH_JPEG:BOOL={0}'.format((
                'ON' if '+jpeg' in spec else 'OFF')),
            '-DWITH_OPENCL:BOOL={0}'.format((
                'ON' if '+opencl' in spec else 'OFF')),
            '-DWITH_OPENCL_SVM:BOOL={0}'.format((
                'ON' if '+opencl_svm' in spec else 'OFF')),
            '-DWITH_OPENCLAMDFFT:BOOL={0}'.format((
                'ON' if '+openclamdfft' in spec else 'OFF')),
            '-DWITH_OPENCLAMDBLAS:BOOL={0}'.format((
                'ON' if '+openclamdblas' in spec else 'OFF')),
            '-DWITH_OPENMP:BOOL={0}'.format((
                'ON' if '+openmp' in spec else 'OFF')),
            '-DWITH_PTHREADS_PF:BOOL={0}'.format((
                'ON' if '+pthreads_pf' in spec else 'OFF')),
            '-DWITH_PNG:BOOL={0}'.format((
                'ON' if '+png' in spec else 'OFF')),
            '-DWITH_QT:BOOL={0}'.format((
                'ON' if '+qt' in spec else 'OFF')),
            '-DWITH_TIFF:BOOL={0}'.format((
                'ON' if '+tiff' in spec else 'OFF')),
            '-DWITH_VTK:BOOL={0}'.format((
                'ON' if '+vtk' in spec else 'OFF')),
            '-DWITH_PROTOBUF:BOOL={0}'.format((
                'ON' if '@3.3.0: +dnn' in spec else 'OFF')),
            '-DBUILD_PROTOBUF:BOOL=OFF',
        ])

        # Media I/O
        if '+zlib' in spec:
            zlib = spec['zlib']
            args.extend([
                '-DZLIB_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if 'build_type=Debug' in spec else 'RELEASE'),
                    zlib.libs[0]),
                '-DZLIB_INCLUDE_DIR:PATH={0}'.format(
                    zlib.headers.directories[0])
            ])

        if '+png' in spec:
            libpng = spec['libpng']
            args.extend([
                '-DPNG_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if 'build_type=Debug' in spec else 'RELEASE'),
                    libpng.libs[0]),
                '-DPNG_INCLUDE_DIR:PATH={0}'.format(
                    libpng.headers.directories[0])
            ])

        if '+jpeg' in spec:
            libjpeg = spec['jpeg']
            args.extend([
                '-DBUILD_JPEG:BOOL=OFF',
                '-DJPEG_LIBRARY:FILEPATH={0}'.format(libjpeg.libs[0]),
                '-DJPEG_INCLUDE_DIR:PATH={0}'.format(
                    libjpeg.headers.directories[0])
            ])

        if '+tiff' in spec:
            libtiff = spec['libtiff']
            args.extend([
                '-DTIFF_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if 'build_type=Debug' in spec else 'RELEASE'),
                    libtiff.libs[0]),
                '-DTIFF_INCLUDE_DIR:PATH={0}'.format(
                    libtiff.headers.directories[0])
            ])

        if '+jasper' in spec:
            jasper = spec['jasper']
            args.extend([
                '-DJASPER_LIBRARY_{0}:FILEPATH={1}'.format((
                    'DEBUG' if 'build_type=Debug' in spec else 'RELEASE'),
                    jasper.libs[0]),
                '-DJASPER_INCLUDE_DIR:PATH={0}'.format(
                    jasper.headers.directories[0])
            ])

        # GUI
        if '+gtk' not in spec:
            args.extend([
                '-DWITH_GTK:BOOL=OFF',
                '-DWITH_GTK_2_X:BOOL=OFF'
            ])
        elif '^gtkplus@3:' in spec:
            args.extend([
                '-DWITH_GTK:BOOL=ON',
                '-DWITH_GTK_2_X:BOOL=OFF'
            ])
        elif '^gtkplus@2:3' in spec:
            args.extend([
                '-DWITH_GTK:BOOL=OFF',
                '-DWITH_GTK_2_X:BOOL=ON'
            ])

        # Python
        if '+python' in spec:
            python_exe = spec['python'].command.path
            python_lib = spec['python'].libs[0]
            python_include_dir = spec['python'].headers.directories[0]

            if '^python@3:' in spec:
                args.extend([
                    '-DBUILD_opencv_python3=ON',
                    '-DPYTHON3_EXECUTABLE={0}'.format(python_exe),
                    '-DPYTHON3_LIBRARY={0}'.format(python_lib),
                    '-DPYTHON3_INCLUDE_DIR={0}'.format(python_include_dir),
                    '-DBUILD_opencv_python2=OFF',
                ])
            elif '^python@2:3' in spec:
                args.extend([
                    '-DBUILD_opencv_python2=ON',
                    '-DPYTHON2_EXECUTABLE={0}'.format(python_exe),
                    '-DPYTHON2_LIBRARY={0}'.format(python_lib),
                    '-DPYTHON2_INCLUDE_DIR={0}'.format(python_include_dir),
                    '-DBUILD_opencv_python3=OFF',
                ])
        else:
            args.extend([
                '-DBUILD_opencv_python2=OFF',
                '-DBUILD_opencv_python3=OFF'
            ])

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            "libopencv_*", root=self.prefix, shared=shared, recursive=True
        )
