import os
from conan import ConanFile
from conan.errors import ConanException
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Git

class HelloConan(ConanFile):
    name = "hello"
    version = "1.0.0"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/simbahebinbo/conan-hello.git"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        source_folder = os.path.join(self.source_folder, "hello")
        if not os.path.exists(source_folder):
            self.output.info(f"Cloning repository into '{source_folder}'")
            self.run(f"git clone https://github.com/simbahebinbo/hello.git {source_folder}")
        else:
            self.output.info(f"Source folder '{source_folder}' already exists, skipping clone.")

        self.output.info("Pulling latest changes")
        self.run(f"git -C {source_folder} pull")


    def build(self):
        build_script_folder = os.path.join(self.source_folder, "hello")
        self.output.info(f"Build script folder: {build_script_folder}")
        if not os.path.exists(build_script_folder):
            raise ConanException(f"Build script folder '{build_script_folder}' does not exist!")
        cmake = CMake(self)
        cmake.configure(build_script_folder=build_script_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        self.output.info(f"Package folder: {self.package_folder}")
        include_folder = os.path.join(self.package_folder, "include")
        lib_folder = os.path.join(self.package_folder, "lib")

        # 头文件路径
        build_include_folder = os.path.join(self.source_folder, "hello/include")

        # 库文件路径
        build_lib_folder = os.path.join(self.build_folder, "src")

        if not os.path.exists(build_lib_folder):
            self.output.warning(f"Source folder '{build_lib_folder}' does not exist!")

        if not os.path.exists(build_include_folder):
            self.output.warning(f"Include folder '{build_include_folder}' does not exist!")

        copy(self, "*.hpp", src=build_include_folder, dst=include_folder)
        copy(self, "*.a", src=build_lib_folder, dst=lib_folder)

    def package_info(self):
        self.cpp_info.libs = ["hello"]