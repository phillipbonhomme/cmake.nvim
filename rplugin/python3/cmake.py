import neovim
from pathlib import Path
import subprocess

# 1. Determine if Clean or Dirty
#    a. Clean - Goto Step #2
#    b. Dirty - Delete all Old Build Files
# 2. Run CMake Project Configuration
#    a. Passes - Goto Step #3
#    b. Fails - Delete all Old Build Files
# 3. Setup RTags Daemon
#    a. Passes - Goto Step #4
#    b. Fails - Kill Daemon & Repeat Step #3
# 4. Setup RTags Client
#    a. Passes - Done!
#    b. Fails - Kill Daemon & Exit
cmake_build_info = {
    "old_cmake_files": [Path("CMakeCache.txt"), Path("cmake_install.cmake")],
    "old_cmake_dir": Path("CMakeFiles"),
    "cmake_proj": Path("CMakeLists.txt"),
    "makefile": Path("Makefile"),
    "build_dir": Path("build"),
    "comp_data_cmake": Path("build/compile_commands.json"),
    "comp_data_bear": Path("compile_commands.json")}

cmake_cmd_info = {
    "cmake_cmd": ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", ".."],
    "rdm_cmd": ["rdm", "--silent", "--daemon"],
    "rc_cmd": ["rc", "-J", "build"]}


@neovim.plugin
class CMake(object):
    def __init__(self, vim):
        self.vim = vim

    def run_cmake(self):
        try:
            subprocess.call(["mkdir", "build"])
        except OSError:
            self.vim.command('echo "Can\'t setup CMake build directory."')
            raise
        try:
            subprocess.call([self.cmake_cmd], cwd="build")
        except OSError:
            self.vim.command('echo "CMake Failed."')
            raise
        if cmake_build_info["comp_data_cmake"].is_file():
            try:
                subprocess.call([self.rdm_cmd], cwd="..")
            except OSError:
                self.vim.command('echo "Couldn\'t start the RTags daemon."')
                raise
            subprocess.call([self.rc_cmd])
        else:
            self.vim.command(
                'echo "Error Generating Compilation Database With CMake"')
            raise

    @neovim.function('CMakeCompDB')
    def cMakeCompDB(self, args):
        self.vim.command('echo "Starting CMake Project"')

        if cmake_build_info["old_cmake_dir"].is_dir():
            subprocess.call(
                ["rm", "-rf", str(cmake_build_info["old_cmake_dir"])])

        if cmake_build_info["comp_data_bear"].is_file():
            subprocess.call(["rm", str(cmake_build_info["comp_data_bear"])])

        for path in cmake_build_info["old_cmake_files"]:
            if path.is_file():
                subprocess.call(["rm", str(path)])

        if cmake_build_info["cmake_proj"].is_file():
            if cmake_build_info["build_dir"].is_dir():
                self.vim.command('echo "Cleaning up Build Directory"')
                subprocess.call(["rm", "-rf", "build"])
            self.vim.command('echo "Running CMake"')
            self.run_cmake()
        else:
            self.vim.command('echo "Not a CMake Project"')
            if cmake_build_info["makefile"].is_file():
                self.run_bear()
            else:
                self.vim.command('echo "Not Setup for Autotools Either"')

