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
    "rc_cmd": ["rc", "-J", str(cmake_build_info["build_dir"])]}


@neovim.plugin
class CMake(object):
    def __init__(self, vim):
        self.vim = vim

    def removeDirtyDir(self):
        if cmake_build_info["old_cmake_dir"].is_dir():
            self.vim.command('echo "Cleaning up Old CMake Directory"')
            subprocess.call(
                ["rm", "-rf", str(cmake_build_info["old_cmake_dir"])])
        if cmake_build_info["build_dir"].is_dir():
            self.vim.command('echo "Cleaning up Build Directory"')
            subprocess.call(
                ["rm", "-rf", str(cmake_build_info["build_dir"])])

    def removeOldCMakeFiles(self):
        for path in cmake_build_info["old_cmake_files"]:
            if path.is_file():
                self.vim.command('echo "Cleaning up Old CMake Files"')
                subprocess.call(["rm", str(path)])

    def run_cmake(self):
        self.vim.command('echo "Running CMake"')
        try:
            subprocess.check_call(["mkdir", "build"])
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.vim.command('echo "Can\'t setup CMake build directory."')
            raise

        try:
            subprocess.check_call([cmake_cmd_info["cmake_cmd"]], cwd="build")
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.vim.command('echo "CMake Failed."')
            raise
        else:
            self.vim.command(
                'echo "Error Generating Compilation Database With CMake"')
            raise

    def setup_rtags_daemon(self):
        self.vim.command('echo "Initializing RTags Daemon"')
        try:
            subprocess.check_call([cmake_cmd_info["rdm_cmd"]], cwd="..")
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.vim.command('echo "Couldn\'t start the RTags daemon."')
            raise

    def connect_rtags_client(self):
        self.vim.command('echo "Connecting RTags Client"')
        if cmake_build_info["comp_data_cmake"].is_file():
            try:
                subprocess.check_call([cmake_cmd_info["rc_cmd"]])
            except subprocess.CalledProcessError as e:
                print(e.output)
                self.vim.command('echo "Couldn\'t connect the RTags client."')
                raise
        else:
            self.vim.command(
                'echo "Error Generating Compilation Database With CMake"')

    @neovim.function('CMakeCompDB')
    def cMakeCompDB(self, args):

        if cmake_build_info["build_dir"].is_dir():
            removeDirtyDir()

        if cmake_build_info["cmake_proj"].is_file():
            self.vim.command('echo "Starting CMake Project"')
            self.run_cmake()
            self.setup_rtags_daemon()
            self.connect_rtags_client()
        else:
            self.vim.command('echo "Not a CMake Project"')

