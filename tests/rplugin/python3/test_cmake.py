from rplugin.python3 import cmake
from unittest import TestCase as utTestCase
from unittest.mock import Mock as utMock
from unittest import main as utmain
from pathlib import Path
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
nvim_remote_socket = Path(NVIM_LISTEN_ADDRESS)


class TestCMake(utTestCase):
    def setUp(self):
        #self.nvim_remote_socket = Path("/tmp/nvimsocket")
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
        print("Setup for CMake unit test")
        #if nvim_remote_socket.is_file():
        #    subprocess.call(["rm", str(nvim_remote_socket)])
        #subprocess.call(["touch", str(nvim_remote_socket)])
        #os.environ["NVIM_LISTEN_ADDRESS"] = str(nvim_remote_socket)
        #self.nvimproc = subprocess.Popen(
        #    ["nvim", "--headless", "-c", "\"terminal python3\""])
        #nvim = neovim.attach('socket', path=NVIM_LISTEN_ADDRESS)
        #self.cmake_plugin = cmake.Main(nvim)

    def tearDown(self):
        print("Teardown for CMake unit test")
        try:
            os.chdir("../../../..")
        except OSError:
            print("Test Error: Couldn't cd out of test directory")
            raise
        #self.nvimproc.terminate()
        #del os.environ["NVIM_LISTEN_ADDRESS"]
        #if nvim_remote_socket.is_file():
        #    subprocess.call(["rm", str(nvim_remote_socket)])

    def test_InitClean(self):
        #build_area = utMock()
        try:
            os.chdir("tests/rplugin/python3/clean")
        except OSError:
            print("Test Error: Couldn't cd into 'clean'")
            raise
        for path in cmake.cmake_build_info["old_cmake_files"]:
            self.assertFalse(path.is_file())
        self.assertFalse(cmake.cmake_build_info["old_cmake_dir"].is_dir())

    def test_initDirty(self):
        subprocess.call(["ls"])
        try:
            os.chdir("tests/rplugin/python3/dirty")
        except OSError:
            print("Test Error: Couldn't cd into 'dirty'")
            raise
        try:
            os.chdir(str(cmake.cmake_build_info["build_dir"]))
        except OSError:
            print("Test Error: Couldn't cd into build directory")
            raise
        for path in cmake.cmake_build_info["old_cmake_files"]:
            if path != Path("compile_commands.json"):
                self.assertTrue(path.is_file())
        self.assertTrue(cmake.cmake_build_info["old_cmake_dir"].is_dir())


if __name__ == '__main__':
    utmain()
