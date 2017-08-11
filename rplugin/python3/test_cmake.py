from unittest import TestCase as utTestCase
from unittest.mock import Mock as utMock
from unittest import main as utmain
import cmake
import neovim
import subprocess
#import os

#nvim = neovim.attach('socket', path=os.environ['NVIM_LISTEN_ADDRESS'])


class TestCMake(utTestCase):
    def setUp(self):
        print("Setup for CMake unit test")
        #self.cmake_plugin = cmake.CMake(nvim)

    def tearDown(self):
        print("Teardown for CMake unit test")

    def test_InitClean(self):
        build_area = utMock()
        for path in cmake.cmake_build_info["old_cmake_files"]:
            self.assertFalse(path.is_file())


if __name__ == '__main__':
    utmain()
