import neovim
from pathlib import Path
import subprocess
import os

@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    def run_cmake():
        try:
            subprocess.call( ["mkdir", "build"] )
        except OSError:
            print('Can\'t setup CMake build directory.')
            raise
        try:
            subprocess.call( ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=1", ".."], cwd="build" )
        except:
            print('CMake Failed.')
            raise
        if comp_data_cmake.is_file():
            try:
                subprocess.call( ["rdm", "--silent", "--daemon"], cwd=".." )
            except:
                print('Couldn\'t start the RTags daemon.')
                raise
            subprocess.call( ["rc", "-J", "build"] )
        else:
            print('Error Generating Compilation Database With CMake')
            raise

    def run_bear():
        try:
            subprocess.call(["bear", "make"])
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print('No Makefile for Bear to Use')
            else:
                print('Bear Error')
            raise
        if comp_data_bear.is_file():
            subprocess.call(["rdm", "--log-file=$HOME/dev/logs/rdm.log", "--silent", "--daemon"])
            subprocess.call(["rc", "-J", "."])
        else:
            print('Error Generating Compilation Database With Bear')

    @neovim.function('CMakeCompDB')
    def CMakeCompDB(self, args):
        self.vim.command('echo "Starting CMake Project"')

        old_cmake_files = [ Path("CMakeCache.txt"), Path("cmake_install.cmake") ]
        old_cmake_dir = Path("CMakeFiles")
        cmake_proj = Path("CMakeLists.txt")
        makefile = Path("Makefile")
        build_dir = Path("build")
        comp_data_cmake = Path("build/compile_commands.json")
        comp_data_bear = Path("compile_commands.json")

        if old_cmake_dir.is_dir():
            subprocess.call( ["rm", "-rf", str( old_cmake_dir ) ] )

        if comp_data_bear.is_file():
            subprocess.call( ["rm", str( comp_data_bear ) ] )

        for path in old_cmake_files:
            if path.is_file():
                subprocess.call(["rm", str( path )])

        if cmake_proj.is_file():
            if build_dir.is_dir():
                print('Cleaning up Build Directory')
                subprocess.call(["rm", "-rf", "build"])
            print('Running CMake')
            run_cmake()
        else:
            print('Not a CMake Project')
            if makefile.is_file():
                run_bear()
            else:
                print('Not Setup for Autotools Either')

