let g:neomake_cmpcmddb_maker = {
    \ 'exe': 'CMakeCompDB',
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmpcmddb<CR>
function CMakeTargets()
    echo "Get CMake Targets"
endfunction
