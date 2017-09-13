from pathlib import Path
import subprocess


class CMakeRTagsPlugin(object):
    def __init__(self):
        self.cmake_build_info = {
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

        self.cmake_cmd_info = {
            "cmake_cmd": ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=1", ".."],
            "rdm_cmd": [
                "rdm", "--silent", "--daemon", "--no-startup-project",
                "--job-count=4"
            ],
            "rdm_cmd_config": [
                "rdm", "--watch-sources-only", "--completion-cache-size=15",
                "--max-include-completion-depth=5"
            ],
            "rtags_cleanup": ["rc", "--clear"],
            "rtags_status": ["rc", "--status"],
            "rtags_file_status": ["rc", "--is-indexed"],
            "rtags_shutdwn": ["rc", "--quit-rdm"],
            "rtags_buffer": ["rc", "--set-buffers"],
            "rtags_buffers": ["rc", "--list-buffers"],
            "rtags_file": ["rc", "--current-file"],
            "rtags_goto": [
                "rc", "--absolute-path", "--containing-function",
                "--follow-location"
            ],
            "rtags_ref": [
                "rc", "--absolute-path", "--wildcard-symbol-names",
                "--all-references", "--containing-function",
                "--references-name"
            ],
            "rtags_sym": [
                "rc", "--absolute-path,"
                "--wildcard-symbol-names", "--containing-function",
                "--cursor-kind", "--find-symbols \"*\""
            ],
            "rc_cmd": ["rc", "-J",
                       str(self.cmake_build_info["build_dir"])]
        }

    def removeDirtyDir(self):
        if self.cmake_build_info["build_dir"].is_dir():
            print("Cleaning up Build Directory")
            subprocess.call(
                ["rm", "-rf",
                 str(self.cmake_build_info["build_dir"])],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

    def removeOldCMakeFiles(self):
        if self.cmake_build_info["old_cmake_dir"].is_dir():
            print("Cleaning up Old CMake Directory")
            subprocess.call(
                ["rm", "-rf",
                 str(self.cmake_build_info["old_cmake_dir"])],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        for path in self.cmake_build_info["old_cmake_files"]:
            if path.is_file():
                print("Cleaning up Old CMake Files")
                subprocess.call(
                    ["rm", str(path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)

    def run_cmake(self):
        print("Running CMake")
        build_dir_cmd_out = subprocess.call(
            ["mkdir", "build"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if build_dir_cmd_out != 0:
            print("Can\'t setup CMake build directory.")
            return

        if self.cmake_build_info["build_dir"].is_dir():
            try:
                subprocess.check_output(
                    self.cmake_cmd_info["cmake_cmd"],
                    cwd=str(self.cmake_build_info["build_dir"]))
            except subprocess.CalledProcessError as e:
                print(e.output)
            if not self.cmake_build_info["comp_data_cmake"].is_file():
                print("Couldn't setup CMake Project")
                return
        else:
            print("Couldn't setup CMake Project")
            return

    def setup_rtags_daemon(self):
        print("Initializing RTags Daemon")
        try:
            subprocess.check_output(
                self.cmake_cmd_info["rtags_shutdwn"],
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)

        try:
            subprocess.check_call(
                self.cmake_cmd_info["rdm_cmd"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise

    def connect_rtags_client(self):
        print("Connecting RTags Client")
        if self.cmake_build_info["comp_data_cmake"].is_file():
            rtags_clt_cmd_out = subprocess.call(
                self.cmake_cmd_info["rc_cmd"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            if rtags_clt_cmd_out != 0:
                print("Info: RTags Daemon Not Running")
                return
        else:
            print("Error Generating Compilation Database With CMake")
            return

    def shutdown_rtags_daemon(self):
        print("Shutting down RTags Daemon")
        try:
            subprocess.call(
                self.cmake_cmd_info["rtags_shutdwn"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)

    def rtags_set_file(self, arg):
        current_buffer = arg
        try:
            subprocess.call(
                self.cmake_cmd_info["rtags_file"] + current_buffer,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)

    def update_rtags_buffers(self, args):
        buffers = args
        cpp_buffers = []
        for buffer in buffers:
            if str(buffer)[-4:] in ['.cpp', '.cc', '.c', '.h', '.hpp']:
                cpp_buffers.append(buffer)
        try:
            subprocess.call(
                self.cmake_cmd_info["rtags_buffer"] + cpp_buffers,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)

    #@classmethod
    def format_rtags(self, tag):
        """
        Tag Format:
        tag[-1] moderncpp_unittest/c3/18/Tweet.h:25:4:
        tag[-2] Tweet(const std::string& message="",
        tag[-3] Tweet::Tweet
        tag[-4] CXXConstructor
        tag[-5] function: class Tweet
        """

        tag_type = len(tag)
        funcstr = ""
        typestr = ""
        namestr = ""
        linecodestr = ""
        filepathstr = ""
        if tag_type is 2:
            linecodestr = tag[0]
            filepathstr = tag[1]
        elif tag_type is 3:
            func = tag[0]
            funcstr = func.split(" ", 1)[1]
            linecodestr = tag[-2]
            filepathstr = tag[-1]
        elif tag_type is 4:
            typestr = tag[0]
            namestr = tag[1]
            linecodestr = tag[-2]
            filepathstr = tag[-1]
        elif tag_type is 5:
            func = tag[0]
            funcstr = func.split(" ", 1)[1]
            typestr = tag[1]
            namestr = tag[2]
            linecodestr = tag[-2]
            filepathstr = tag[-1]
        tagstr = [typestr, namestr, funcstr, linecodestr, filepathstr]
        return '\t'.join(tagstr)

    def rtags_tagrun(self, cmd):
        try:
            tagrun = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)
        taglines = tagrun.split("\n")
        tags = map(split("\t"), taglines)
        tags[:] = map(reverse(), tags)
        tags[:] = map(self.format_rtags, tags)
        return tags
