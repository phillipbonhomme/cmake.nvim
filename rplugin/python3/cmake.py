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
    "cmake_cmd": ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=1", ".."],
    "rdm_cmd":
    ["rdm", "--silent", "--daemon", "--no-startup-project", "--job-count=4"],
    "rdm_cmd_config": [
        "rdm", "--watch-sources-only", "--completion-cache-size=15",
        "--max-include-completion-depth=5"
    ],
    "rtags_cleanup": ["rc", "--clear"],
    "rtags_status": ["rc", "--status"],
    "rtags_file_status": ["rc", "--is-indexed"],
    "rtags_shutdwn": ["rc", "--quit-rdm"],
    "rtags_buffer": ["rc", "--set-buffer"],
    "rtags_buffers": ["rc", "--list-buffers"],
    "rtags_file": ["rc", "--current-file"],
    "rc_cmd": ["rc", "-J", str(cmake_build_info["build_dir"])]
}

plugin_cmd_info = {
    "chromatica": "ChromaticaStart",
    "deoplete": "call deoplete#enable()"
}


def removeDirtyDir():
    if cmake_build_info["build_dir"].is_dir():
        print("Cleaning up Build Directory")
        subprocess.call(
            ["rm", "-rf", str(cmake_build_info["build_dir"])],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)


def removeOldCMakeFiles():
    if cmake_build_info["old_cmake_dir"].is_dir():
        print("Cleaning up Old CMake Directory")
        subprocess.call(
            ["rm", "-rf", str(cmake_build_info["old_cmake_dir"])],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    for path in cmake_build_info["old_cmake_files"]:
        if path.is_file():
            print("Cleaning up Old CMake Files")
            subprocess.call(
                ["rm", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)


def run_cmake():
    print("Running CMake")
    build_dir_cmd_out = subprocess.call(
        ["mkdir", "build"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    if build_dir_cmd_out != 0:
        print("Can\'t setup CMake build directory.")
        return

    if cmake_build_info["build_dir"].is_dir():
        try:
            subprocess.check_output(
                cmake_cmd_info["cmake_cmd"],
                cwd=str(cmake_build_info["build_dir"]),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)
        if not cmake_build_info["comp_data_cmake"].is_file():
            print("Couldn't setup CMake Project")
            return
    else:
        print("Couldn't setup CMake Project")
        return


def setup_rtags_daemon():
    print("Initializing RTags Daemon")
    try:
        subprocess.check_output(
            cmake_cmd_info["rtags_shutdwn"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(e.output)

    try:
        subprocess.check_call(
            cmake_cmd_info["rdm_cmd"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise


def connect_rtags_client():
    print("Connecting RTags Client")
    if cmake_build_info["comp_data_cmake"].is_file():
        rtags_clt_cmd_out = subprocess.call(
            cmake_cmd_info["rc_cmd"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if rtags_clt_cmd_out != 0:
            print("Info: RTags Daemon Not Running")
            return
    else:
        print("Error Generating Compilation Database With CMake")
        return


def shutdown_rtags_daemon():
    print("Shutting down RTags Daemon")
    try:
        subprocess.call(
            cmake_cmd_info["rtags_shutdwn"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(e.output)


def rtags_set_file(arg):
    current_buffer = arg
    try:
        subprocess.call(
            cmake_cmd_info["rtags_file"] + current_buffer,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(e.output)


def update_rtags_buffers(args):
    buffers = args
    cpp_buffers = []
    for buffer in buffers:
        if str(buffer)[-4:] in ['.cpp', '.cc', '.c', '.h', '.hpp']:
            cpp_buffers.append(buffer)
    try:
        subprocess.call(
            cmake_cmd_info["rtags_buffer"] + cpp_buffers,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(e.output)


@neovim.plugin
class CMakeRTagsProject(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.command('CMakeProjectSetup', sync=False)
    def run_cmake_setup_rtags(self):
        removeOldCMakeFiles()
        if cmake_build_info["build_dir"].is_dir():
            removeDirtyDir()

        if cmake_build_info["cmake_proj"].is_file():
            self.vim.command('echo "Starting CMake Project"')
            run_cmake()
            setup_rtags_daemon()
            connect_rtags_client()
            for plugin, cmd in plugin_cmd_info.items():
                self.vim.command(cmd)
        else:
            self.vim.command('echo "Not a CMake Project"')

    @neovim.command('CMakeProjectTeardown', sync=False)
    def run_cmake_teardown_rtags(self):
        shutdown_rtags_daemon()

    @neovim.command('CMakeProjectSetFile', nargs='1', sync=True)
    def run_rtags_set_file(self, arg):
        rtags_set_file(arg)

    @neovim.command('CMakeProjectUpdateBuffers', sync=False)
    def run_update_rtags_buffers(self):
        buffers = self.vim.buffers
        update_rtags_buffers(buffers)

