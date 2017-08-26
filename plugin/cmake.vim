"function! GetCompDB()
"    exec CMakeCompDB()
"endfunc
"let FnCMakeCompDB = function("GetCompDB")
"let funccmakecompdb = string(FnCMakeCompDB)
"let RunCMakeCompDB = function('GetCompDB')
"   let self.fn = function("GetCompDB")
"function cmake.run() dict
"   let self.fn = FnCMakeCompDB
"endfunction
"let g:neomake_cmakecompdb_maker = {
"    \ 'exe': string(FnCMakeCompDB),
"    \ 'args': [''] 
"    \ }
"noremap <unique> <Plug>GenerateCompDB :exec CMakeCompDB()<CR>
"noremap <unique> <Plug>CMakeProjectSetup :CMakeProjectSetup<CR>
function! CMakeTargets()
    echo "Get CMake Targets"
endfunction
" RTags Setup
if !exists("g:rtags_client_command")
    let g:rtags_client_command = "rc"
endif
"function! UpdateRTagsBuffers()
"    execute "!" . g:rtags_client_command . " --add-buffers" . bufname("%")
"endfunction
autocmd FileType cpp :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType cc :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType c :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType hpp :CMakeProjectSetFile expand('%:p')<CR>
autocmd FileType h :CMakeProjectSetFile expand('%:p')<CR>
"autocmd FileType cpp :CMakeProjectUpdateBuffers<CR>
"autocmd FileType cc :CMakeProjectUpdateBuffers<CR>
"autocmd FileType c :CMakeProjectUpdateBuffers<CR>
"autocmd FileType hpp :CMakeProjectUpdateBuffers<CR>
"autocmd FileType h :CMakeProjectUpdateBuffers<CR>
"autocmd FileType cpp :call UpdateRTagsBuffers()
"autocmd FileType cc :call UpdateRTagsBuffers()
"autocmd FileType c :call UpdateRTagsBuffers()
"autocmd FileType hpp :call UpdateRTagsBuffers()
"autocmd FileType h :call UpdateRTagsBuffers()
