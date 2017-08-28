function! CMakeTargets()
    echo "Get CMake Targets"
endfunction
" RTags Setup
if !exists("g:rtags_client_command")
    let g:rtags_client_command = "rc"
endif
autocmd FileType cpp :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType cc :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType c :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType hpp :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType h :CMakeProjectSetFile expand('%:p')<CR>
source 'plugin/rtags.vim'
