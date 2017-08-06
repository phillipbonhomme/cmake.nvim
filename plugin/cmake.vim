echo "Starting CMake.nvim"
let g:neomake_cmpcmddb_maker = {
    \ 'exe': 'CMakeCompDB',
    \ 'args': [''] 
    \ }
noremap <unique> <Plug>NeomakeCompDB :Neomake! cmpcmddb<CR>
function DoItVimL()
    echo "hello from DoItVimL"
endfunction
