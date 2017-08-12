import neovim
from pathlib import Path
import subprocess

cmake_build_info = {
    "old_cmake_files": [
        Path("CMakeCache.txt"),
        Path("cmake_install.cmake"),
        Path("Makefile"),
        Path("compile_commands.json")],
    "old_cmake_dir": Path("CMakeFiles"),
    "cmake_proj": Path("CMakeLists.txt"),
    "build_dir": Path("build"),
    "comp_data_cmake": Path("build/compile_commands.json")}

cmake_cmd_info = {
    "cmake_cmd": ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", ".."],
    "rdm_cmd": ["rdm", "--silent", "--daemon"],
    "rc_cmd": ["rc", "-J", str(cmake_build_info["build_dir"])]}


@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    def removeDirtyDir(self):
        if cmake_build_info["build_dir"].is_dir():
            self.vim.command('echo "Cleaning up Build Directory"')
            subprocess.call(
                ["rm", "-rf", str(cmake_build_info["build_dir"])])

    def removeOldCMakeFiles(self):
        if cmake_build_info["old_cmake_dir"].is_dir():
            self.vim.command('echo "Cleaning up Old CMake Directory"')
            subprocess.call(
                ["rm", "-rf", str(cmake_build_info["old_cmake_dir"])])
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

    @neovim.function('CMakeCompDB', sync=True)
    def CMakeCompDB(self):
        self.removeOldCMakeFiles()
        if cmake_build_info["build_dir"].is_dir():
            self.removeDirtyDir()

        if cmake_build_info["cmake_proj"].is_file():
            self.vim.command('echo "Starting CMake Project"')
            self.run_cmake()
            self.setup_rtags_daemon()
            self.connect_rtags_client()
        else:
            self.vim.command('echo "Not a CMake Project"')
