function! GetCompDB()
    exec CMakeCompDB()
endfunc
let g:neomake_cmakecompdb_maker = {
    \ 'exe': function('GetCompDB'),
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmakecompdb<CR>
function CMakeTargets()
    echo "Get CMake Targets"
endfunction
