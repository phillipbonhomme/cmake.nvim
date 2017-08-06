let GetCompDB = function('CMakeCompDB')
let g:neomake_cmakecompdb_maker = {
    \ 'exe': 'GetCompDB',
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmakecompdb<CR>
function CMakeTargets()
    echo "Get CMake Targets"
endfunction
