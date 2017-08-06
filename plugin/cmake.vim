function! GetCompDB()
    exec CMakeCompDB()
endfunc
let RunCMakeCompDB = function('GetCompDB')
let g:neomake_cmakecompdb_maker = {
    \ 'exe': 'RunCMakeCompDB',
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmakecompdb<CR>
function CMakeTargets()
    echo "Get CMake Targets"
endfunction
