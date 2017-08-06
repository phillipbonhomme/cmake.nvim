function! GetCompDB()
    exec CMakeCompDB()
endfunc
"let FnCMakeCompDB = function("GetCompDB")
"let funccmakecompdb = string(FnCMakeCompDB)
"let RunCMakeCompDB = function('GetCompDB')
"   let self.fn = function("GetCompDB")
function cmake.run() dict
   let self.fn = GetCompDB
endfunction
let g:neomake_cmakecompdb_maker = {
    \ 'exe': string(cmake.run),
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmakecompdb<CR>
function! CMakeTargets()
    echo "Get CMake Targets"
endfunction
