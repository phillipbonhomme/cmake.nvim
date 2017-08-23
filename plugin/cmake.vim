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
function! AddFileToRTagsProject()
    execute "!" . g:rtags_client_command . " --add-buffers " . bufname("%")
endfunction
autocmd FileType cpp :call AddFileToRTagsProject()
autocmd FileType cc :call AddFileToRTagsProject()
autocmd FileType c :call AddFileToRTagsProject()
autocmd FileType hpp :call AddFileToRTagsProject()
autocmd FileType h :call AddFileToRTagsProject()
