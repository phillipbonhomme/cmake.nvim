function! GetCompDB()
    exec CMakeCompDB()
endfunc
let FnCMakeRun = function("GetCompDB")
"let RunCMakeCompDB = function('GetCompDB')
"function cmake.run() dict
"   let self.fn = function('GetCompDB')
"endfunction
let g:neomake_cmakecompdb_maker = {
    \ 'exe': string(FnCMakeRun),
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmakecompdb<CR>
function CMakeTargets()
    echo "Get CMake Targets"
endfunction
