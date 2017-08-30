" Wrap up the remote plugin function(s), as of right now it cannot
" be used as a Funcref.
function! fzf#rtags#source(arg) abort
    call fzf_rtags_source(a:arg)
endfunction
