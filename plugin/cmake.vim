function! GetCompDB()
    exec CMakeCompDB()
endfunc
let FnCMakeCompDB = function("GetCompDB")
let funccmakecompdb = string(FnCMakeCompDB)
"let RunCMakeCompDB = function('GetCompDB')
"function cmake.run() dict
"   let self.fn = function('GetCompDB')
"endfunction
let g:neomake_cmakecompdb_maker = {
    \ 'exe': 'funccmakecompdb',
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmakecompdb<CR>
function! CMakeTargets()
    echo "Get CMake Targets"
endfunction
