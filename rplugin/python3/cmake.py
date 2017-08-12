import neovim
from pathlib import Path
import subprocess

cmake_build_info = {
    "old_cmake_files": [
        Path("CMakeCache.txt"),
        Path("cmake_install.cmake"),
        Path("Makefile"),
        Path("compile_commands.json")
    ],
    "old_cmake_dir":
    Path("CMakeFiles"),
    "cmake_proj":
    Path("CMakeLists.txt"),
    "build_dir":
    Path("build"),
    "comp_data_cmake":
    Path("build/compile_commands.json")
}

cmake_cmd_info = {
    "cmake_cmd": ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", ".."],
    "rdm_cmd": ["rdm", "--silent", "--daemon"],
    "rtags_shutdwn": ["rc", "--quit-rdm"],
    "rc_cmd": ["rc", "-J", str(cmake_build_info["build_dir"])]
}


def removeDirtyDir():
    if cmake_build_info["build_dir"].is_dir():
        print("Cleaning up Build Directory")
        subprocess.call(["rm", "-rf", str(cmake_build_info["build_dir"])])


def removeOldCMakeFiles():
    if cmake_build_info["old_cmake_dir"].is_dir():
        print("Cleaning up Old CMake Directory")
        subprocess.call(["rm", "-rf", str(cmake_build_info["old_cmake_dir"])])
    for path in cmake_build_info["old_cmake_files"]:
        if path.is_file():
            print("Cleaning up Old CMake Files")
            subprocess.call(["rm", str(path)])


def run_cmake():
    print("Running CMake")
    try:
        subprocess.check_call(["mkdir", "build"])
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("Can\'t setup CMake build directory.")
        raise

    subprocess.check_call(cmake_cmd_info["cmake_cmd"], cwd="build")
    if not cmake_build_info["comp_data_cmake"].is_file():
        print("Couldn't setup CMake Project")
    #try:
    #    subprocess.check_call(cmake_cmd_info["cmake_cmd"], cwd="build")
    #except subprocess.CalledProcessError as e:
    #    print(e.output)
    #    print("CMake Failed.")
    #    raise
    #else:
    #    print("Error Generating Compilation Database With CMake")
    #    raise


def setup_rtags_daemon():
    print("Initializing RTags Daemon")
    try:
        subprocess.check_call(cmake_cmd_info["rdm_cmd"], cwd="..")
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("Couldn\'t start the RTags daemon.")
        raise


def connect_rtags_client():
    print("Connecting RTags Client")
    if cmake_build_info["comp_data_cmake"].is_file():
        try:
            subprocess.check_call(cmake_cmd_info["rc_cmd"])
        except subprocess.CalledProcessError as e:
            print(e.output)
            print("Couldn\'t connect the RTags client.")
            raise
    else:
        print("Error Generating Compilation Database With CMake")


@neovim.plugin
class CMakeRTagsProject(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.command('CMakeProjectSetup', sync=True)
    def run_cmake_setup_rtags(self):
        removeOldCMakeFiles()
        if cmake_build_info["build_dir"].is_dir():
            removeDirtyDir()

        if cmake_build_info["cmake_proj"].is_file():
            self.vim.command('echo "Starting CMake Project"')
            run_cmake()
            setup_rtags_daemon()
            connect_rtags_client()
            self.vim.command('ChromaticaStart')
        else:
            self.vim.command('echo "Not a CMake Project"')
