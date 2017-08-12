from rplugin.python3 import cmake
from unittest import TestCase as utTestCase
from unittest.mock import Mock as utMock
from unittest import main as utmain
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


class TestCMake(utTestCase):
    def setUp(self):
        print("Setup for CMake unit test")
        subprocess.call(["touch", "/tmp/nvimsocket"])
        os.environ["NVIM_LISTEN_ADDRESS"] = "/tmp/nvimsocket"
        #subprocess.call(["nvim", "--embed", "-c", "\"terminal python3\""])
        self.nvimproc = subprocess.Popen(
            ["nvim", "--headless", "-c", "\"terminal python3\""])
        nvim = neovim.attach('socket', path=os.environ['NVIM_LISTEN_ADDRESS'])
        self.cmake_plugin = cmake.Main(nvim)

    def tearDown(self):
        print("Teardown for CMake unit test")
        self.nvimproc.terminate()
        del os.environ["NVIM_LISTEN_ADDRESS"]

    def test_InitClean(self):
        #build_area = utMock()
        try:
            os.chdir("tests/rplugin/python3/clean")
        except OSError:
            print("Test Error: Couldn't cd into 'clean'")
            raise
        for path in cmake.cmake_build_info["old_cmake_files"]:
            self.assertFalse(path.is_file())
        self.assertFalse(cmake.cmake_build_info["old_cmake_dir"].is_file())


if __name__ == '__main__':
    utmain()
