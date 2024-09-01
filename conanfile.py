import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import copy

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
        git = Git(self)
        if not os.path.exists(os.path.join(self.source_folder, ".git")):
            git.clone("https://github.com/simbahebinbo/hello.git", target=".")
        else:
            self.run("git pull")

        # 检查分支或标签是否正确（可选）
        git.checkout("master")

    def build(self):
        build_script_folder=os.path.join(self.source_folder)
        self.run(f"cmake {build_script_folder}")
        self.run("cmake --build .")

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # 头文件路径
        include_folder = os.path.join(self.source_folder, "include")
        # 库文件路径
        lib_folder = os.path.join(self.build_folder, "src")

        # 使用 conan.tools.files.copy 替代 self.copy
        copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include"), src=include_folder)
        copy(self, "*.a", dst=os.path.join(self.package_folder, "lib"), src=lib_folder)

    def package_info(self):
        self.cpp_info.libs = ["hello"]