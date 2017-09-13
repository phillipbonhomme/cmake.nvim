import neovim
import json
from ..rtags import rtags


@neovim.plugin
class CMakeRTagsProject(object):
    def __init__(self, vim):
        self.vim = vim
        if self.vim.vars.get("loaded_fzf") == 1:
            self.selectionUI = "fzf"
        else:
            self.selectionUI = "location-list"
        self.plugin_cmd_info = {
            "chromatica": "ChromaticaStart",
            "deoplete": "call deoplete#enable()"
        }
        self.util = rtags.CMakeRTagsPlugin()

    def fzf(self, source, sink) -> None:
        self.asyncCommand("""
call fzf#run(fzf#wrap({{
    'source': {},
    'sink': function('{}')
    }}))
""".replace("\n", "").format(json.dumps(source), sink))
        self.nvim.async_call(self.nvim.feedkeys, "i")

    @neovim.function('fzf_rtags_source')
    def fzf_rtags_source(self, args):
        retVal = []
        cmd = []
        if str(args).find("goto"):
            cursor = self.vim.command('getpos(\'.\')')
            cmd = self.util.cmake_cmd_info["rtags_goto"]
            cmd.extend(
                [self.vim.command('expand(\'%:p\')') + cursor[1] + cursor[2]])
        elif str(args).find("ref"):
            cursor = self.vim.command('expand("<cword>")')
            cmd = self.util.cmake_cmd_info["rtags_ref"]
            cmd.extend([cursor])
        elif str(args).find("sym"):
            cmd = self.util.cmake_cmd_info["rtags_sym"]
        else:
            return None
        retVal = self.util.rtags_tagrun(cmd)
        return retVal

    @neovim.command('CMakeProjectSetup', sync=False)
    def run_cmake_setup_rtags(self):
        self.util.removeOldCMakeFiles()
        if self.util.cmake_build_info["build_dir"].is_dir():
            self.util.removeDirtyDir()

        if self.util.cmake_build_info["cmake_proj"].is_file():
            self.vim.command('echo "Starting CMake Project"')
            self.util.run_cmake()
            self.util.setup_rtags_daemon()
            self.util.connect_rtags_client()
            for plugin, cmd in self.plugin_cmd_info.items():
                self.vim.command(cmd)
        else:
            self.vim.command('echo "Not a CMake Project"')

    @neovim.command('CMakeProjectTeardown', sync=False)
    def run_cmake_teardown_rtags(self):
        self.util.shutdown_rtags_daemon()

    @neovim.command('CMakeProjectSetFile', nargs='1', sync=True)
    def run_rtags_set_file(self, arg):
        self.util.rtags_set_file(arg)

    @neovim.command('CMakeProjectUpdateBuffers', sync=False)
    def run_update_rtags_buffers(self):
        buffers = self.vim.buffers
        self.util.update_rtags_buffers(buffers)
