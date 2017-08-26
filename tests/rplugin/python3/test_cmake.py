from rplugin.python3 import cmake
import unittest
import pathlib
import neovim
import subprocess
import os

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
NVIM_LISTEN_ADDRESS = "/tmp/nvim-CMakePluginTest"
nvim_remote_socket = pathlib.Path(NVIM_LISTEN_ADDRESS)

src_info = {
    "cpp": pathlib.Path("main.cpp"),
    "test_cpp": pathlib.Path("Test.cpp"),
    "cmake": pathlib.Path("CMakeLists.txt")
}


class TestCMake(unittest.TestCase):
    def setUp(self):
        #self.nvim_remote_socket = pathlib.Path("/tmp/nvimsocket")
        #os.environ["NVIM_LISTEN_ADDRESS"] = "/tmp/nvimsocket"
        #subprocess.call(["nvim", "--headless", "-c", "\"terminal python3\""])
        #self.nvimproc = subprocess.Popen(
        #    ["nvim", "--headless", "-c", "\"terminal python3\""])
        #["NVIM_LISTEN_ADDRESS="+str(self.nvim_remote_socket), "nvim", "--headless", "-c", "\"terminal python3\""])
        #try:
        #    nvim = neovim.attach("socket",
        #                        path=os.environ["NVIM_LISTEN_ADDRESS"])
        #except OSError:
        #    print("Can't Launch Neovim in test fixture setup.")
        #    raise
        #if nvim_remote_socket.is_file():
        #    subprocess.call(["rm", str(nvim_remote_socket)])
        #subprocess.call(["touch", str(nvim_remote_socket)])
        #os.environ["NVIM_LISTEN_ADDRESS"] = str(nvim_remote_socket)
        #self.nvimproc = subprocess.Popen(
        #    ["nvim", "--headless", "-c", "\"terminal python3\""])
        #nvim = neovim.attach('socket', path=NVIM_LISTEN_ADDRESS)
        #self.cmake_plugin = cmake.Main(nvim)
        print("Setup for CMake unit test")
        try:
            os.chdir("tests/rplugin/python3")
        except OSError:
            print("Test Error: Couldn't cd into testing directory.")
            raise

    def tearDown(self):
        print("Teardown for CMake unit test")
        try:
            os.chdir("../../../..")
        except OSError:
            print("Test Error: Couldn't cd out of test directory")
            raise
        subprocess.call(cmake.cmake_cmd_info["rtags_shutdwn"])
        #self.nvimproc.terminate()
        #del os.environ["NVIM_LISTEN_ADDRESS"]
        #if nvim_remote_socket.is_file():
        #    subprocess.call(["rm", str(nvim_remote_socket)])

    def test_InitClean(self):
        try:
            os.chdir("clean")
        except OSError:
            print("Test Error: Couldn't cd into 'clean' test directory.")
            raise
        self.assertFalse(cmake.cmake_build_info["build_dir"].is_dir())
        for path in cmake.cmake_build_info["old_cmake_files"]:
            self.assertFalse(path.is_file())
        self.assertFalse(cmake.cmake_build_info["old_cmake_dir"].is_dir())

    def test_initDirty(self):
        try:
            os.chdir("dirty")
        except OSError:
            print("Test Error: Couldn't cd into 'dirty' test directory.")
            raise
        try:
            os.chdir(str(cmake.cmake_build_info["build_dir"]))
        except OSError:
            print("Test Error: Couldn't cd into build directory")
            raise
        self.assertTrue(cmake.cmake_build_info["old_cmake_dir"].is_dir())
        for path in cmake.cmake_build_info["old_cmake_files"]:
            if path != pathlib.Path("compile_commands.json"):
                self.assertTrue(path.is_file())

    def test_RTagsDaemonStartDirty(self):
        try:
            os.chdir("dirty")
        except OSError:
            print("Test Error: Couldn't cd into 'dirty' test directory.")
            raise
        self.assertTrue(cmake.cmake_build_info["build_dir"].is_dir())
        cmake.setup_rtags_daemon()
        try:
            rtags_daemon_status = subprocess.check_output(
                cmake.cmake_cmd_info["rtags_status"])
        except subprocess.CalledProcessError as e:
            print(e.output)
        #try:
        #    rtags_daemon_status = subprocess.check_call(
        #        cmake.cmake_cmd_info["rtags_status"])
        #except subprocess.CalledProcessError as e:
        #    if rtags_daemon_status.returncode != 0:
        #        print(e.output)
        #        print("Test Error: RTags Daemon is not running yet.")
        #        raise

        #self.assertIn(
        #    "*********************************\nfileids\n*********************************\n*********************************\nheadererrors\n*********************************\n*********************************\ninfo\n*********************************\nRunning a release build\nsocketFile: /Users/phillipbonhomme/.rdm\ndataDir: /Users/phillipbonhomme/.cache/rtags/\noptions: 0x14jobCount: 4\nrpVisitFileTimeout: 60000\nrpIndexDataMessageTimeout: 60000\nrpConnectTimeout: 0\nrpConnectTimeout: 0\ndefaultArguments: List<String>(-ferror-limit=50, -Wall, -fspell-checking, -Wno-unknown-warning-option\")\nincludePaths: List<Source::Include>(\")\ndefines: List<Source::Define>(-DRTAGS=\")\nignoredCompilers: Set<Path>(\")\n*********************************\njobs\n*********************************\n",
        #    str(rtags_daemon_status))
        self.assertEqual(
            len("*********************************\nfileids\n*********************************\n*********************************\nheadererrors\n*********************************\n*********************************\ninfo\n*********************************\nRunning a release build\nsocketFile: /Users/phillipbonhomme/.rdm\ndataDir: /Users/phillipbonhomme/.cache/rtags/\noptions: 0x14jobCount: 4\nrpVisitFileTimeout: 60000\nrpIndexDataMessageTimeout: 60000\nrpConnectTimeout: 0\nrpConnectTimeout: 0\ndefaultArguments: List<String>(-ferror-limit=50, -Wall, -fspell-checking, -Wno-unknown-warning-option\")\nincludePaths: List<Source::Include>(\")\ndefines: List<Source::Define>(-DRTAGS=\")\nignoredCompilers: Set<Path>(\")\n*********************************\njobs\n*********************************\n"
                ), len(str(rtags_daemon_status)) - 23)

        #self.assertTrue(cmake.cmake_build_info["comp_data_cmake"].is_file())
        #file_check_out = subprocess.check_call(
        #    [cmake.cmake_cmd_info["rtags_check_file"] + " " +
        #        str(src_info["cpp"])],
        #    stdout=subprocess.STDOUT,
        #    stderr=subprocess.STDERR)
        #self.assertEqual(file_check_out.output, "managed")
        #file_check_out = subprocess.check_call(
        #    [cmake.cmake_cmd_info["rtags_check_file"] + " " +
        #        str(src_info["test_cpp"])],
        #    stdout=subprocess.STDOUT,
        #    stderr=subprocess.STDERR)
        #self.assertEqual(file_check_out.output, "managed")

    #def test_RTagsClientControlBuffers(self):
    #def test_RTagsClientInit(self):
    #def test_RTagsDaemonStop(self):
    #def test_RTagsDaemonRestart(self):
    #def test_RTagsDaemonStart(self):
    #    try:
    #        os.chdir("tests/rplugin/python3/clean")
    #    except OSError:
    #        print("Test Error: Couldn't cd into 'clean'")
    #        raise
    #    cmake.setup_rtags_daemon()
    #    # Assertions


if __name__ == '__main__':
    unittest.main()
