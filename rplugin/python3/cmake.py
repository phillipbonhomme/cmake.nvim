import neovim
from pathlib import Path
import subprocess
import os

@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim
        self.old_cmake_files = [ Path("CMakeCache.txt"), Path("cmake_install.cmake") ]
        self.old_cmake_dir = Path("CMakeFiles")
        self.cmake_proj = Path("CMakeLists.txt")
        self.makefile = Path("Makefile")
        self.build_dir = Path("build")
        self.comp_data_cmake = Path("build/compile_commands.json")
        self.comp_data_bear = Path("compile_commands.json")


    def run_cmake(self):
        try:
            subprocess.call( ["mkdir", "build"] )
        except OSError:
            self.vim.command('echo "Can\'t setup CMake build directory."')
            raise
        try:
            subprocess.call( ["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=1", ".."], cwd="build" )
        except:
            self.vim.command('echo "CMake Failed."')
            raise
        if self.comp_data_cmake.is_file():
            try:
                subprocess.call( ["rdm", "--silent", "--daemon"], cwd=".." )
            except:
                self.vim.command('echo "Couldn\'t start the RTags daemon."')
                raise
            subprocess.call( ["rc", "-J", "build"] )
        else:
            self.vim.command('echo "Error Generating Compilation Database With CMake"')
            raise

    def run_bear(self):
        try:
            subprocess.call(["bear", "make"])
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                self.vim.command('echo "No Makefile for Bear to Use"')
            else:
                self.vim.command('echo "Bear Error"')
            raise
        if self.comp_data_bear.is_file():
            subprocess.call(["rdm", "--log-file=$HOME/dev/logs/rdm.log", "--silent", "--daemon"])
            subprocess.call(["rc", "-J", "."])
        else:
            self.vim.command('echo "Error Generating Compilation Database With Bear"')

    @neovim.function('CMakeCompDB')
    def CMakeCompDB(self, args):
        self.vim.command('echo "Starting CMake Project"')

        if self.old_cmake_dir.is_dir():
            subprocess.call( ["rm", "-rf", str( old_cmake_dir ) ] )

        if self.comp_data_bear.is_file():
            subprocess.call( ["rm", str( comp_data_bear ) ] )

        for path in self.old_cmake_files:
            if path.is_file():
                subprocess.call(["rm", str( path )])

        if self.cmake_proj.is_file():
            if self.build_dir.is_dir():
                self.vim.command('echo "Cleaning up Build Directory"')
                subprocess.call(["rm", "-rf", "build"])
            self.vim.command('echo "Running CMake"')
            self.run_cmake()
        else:
            self.vim.command('echo "Not a CMake Project"')
            if self.makefile.is_file():
                self.run_bear()
            else:
                self.vim.command('echo "Not Setup for Autotools Either"')

