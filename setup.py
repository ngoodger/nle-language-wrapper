#!/usr/bin/env python

import os
import pathlib
import shutil
import subprocess
import sys
from distutils import sysconfig

import setuptools
from setuptools.command import build_ext


class CMakeBuild(build_ext.build_ext):
    def run(self):  # Necessary for pip install -e.
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        source_path = pathlib.Path(__file__).parent.resolve()
        output_path = (
            pathlib.Path(self.get_ext_fullpath(ext.name))
            .parent.joinpath("nle_language_wrapper")
            .resolve()
        )
        os.makedirs(self.build_temp, exist_ok=True)
        cmake_cmd = [
            "cmake",
            str(source_path),
            f"-DPYTHON_SRC_PARENT={source_path}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={sys.base_prefix}",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={output_path}",
            f"-DPYTHON_INCLUDE_DIR={sysconfig.get_python_inc()}",
            f"-DPYTHON_LIBRARY={sysconfig.get_config_var('LIBDIR')}",
        ]
        build_cmd = ["cmake", "--build", ".", "--parallel"]
        install_cmd = ["cmake", "--install", "."]
        subprocess.check_call(
            ["python", "-m", "setup", "build"], cwd=f"{source_path}/nle"
        )
        libnethack_path = list(pathlib.Path("./nle/build").glob("**/libnethack.so"))[0]
        shutil.copy(
            libnethack_path, pathlib.Path("./nle_language_wrapper/libnethack.so")
        )

        subprocess.check_call(cmake_cmd, cwd=self.build_temp)
        subprocess.check_call(build_cmd, cwd=self.build_temp)
        subprocess.check_call(install_cmd, cwd=self.build_temp)


packages = [
    "nle_language_wrapper",
    "nle_language_wrapper.agents",
    "nle_language_wrapper.agents.sample_factory",
    "nle_language_wrapper.scripts",
    "nle_language_wrapper.tests",
    "nle_language_wrapper.wrappers",
]

extras_deps = {
    "dev": [
        "black>=22.6.0",
        "flake8>=4.0.1",
        "pytest>=7.1.2",
        "pytest-cov>=3.0.0",
        "pytest-mock>=3.7.0",
        "pygame>=2.1.2",
        "isort>=5.10.1",
    ],
    "agent": ["sample_factory>=1.121.4", "transformers>=4.17.0"],
}

if __name__ == "__main__":
    PACKAGE_NAME = "nle-language-wrapper"
    cwd = os.path.dirname(os.path.abspath(__file__))

    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

    setuptools.setup(
        name=PACKAGE_NAME,
        version="0.1.3",
        description=("Language Wrapper for the NetHack Learning Environment (NLE) "),
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Nikolaj Goodger",
        url="https://github.com/ngoodger/nle-language-wrapper",
        license="MIT License",
        packages=packages,
        package_data={"": ["nle_language_wrapper/libnethack.so"]},
        include_package_data=True,
        ext_modules=[setuptools.Extension("nle_language_wrapper", sources=[])],
        cmdclass={"build_ext": CMakeBuild},
        setup_requires=["pybind11>=2.9"],
        install_requires=[
            "pybind11>=2.9",
            "numpy>=1.21.0",
            "gym>=0.15,<=0.23",
            "nle>=0.8.1",
            "minihack>=0.1.3",
        ],
        tests_require=["pytest>=7.0.1"],
        extras_require=extras_deps,
        python_requires=">=3.7",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 2 - Pre-Alpha",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: C++",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Games/Entertainment",
        ],
    )
