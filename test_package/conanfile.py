from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
import os

class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    requires = "hello/1.0.0"
    test_type = "explicit"

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not self.settings.os == "Windows":
            self.run(".%sgreet" % os.sep, env="conanrun")