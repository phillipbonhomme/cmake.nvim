" RTags Setup
  if !exists("g:rtags_client_command")
      let g:rtags_client_command = "rc"
  endif
" Autocommands
  autocmd FileType cpp :CMakeProjectSetFile expand('%:p')<CR>
  autocmd FileType cc :CMakeProjectSetFile expand('%:p')<CR>
  autocmd FileType c :CMakeProjectSetFile expand('%:p')<CR>
  autocmd FileType hpp :CMakeProjectSetFile expand('%:p')<CR>
  autocmd FileType h :CMakeProjectSetFile expand('%:p')<CR>
" Mappings
  "noremap <unique> <Plug>RTagsGoTo :RTagsGoTo <CR>
  "noremap <unique> <Plug>RTagsFindRefs :RTagsFindRefs <CR>
  "noremap <unique> <Plug>RTagsFindSymbol :RTagsFindSymbol <CR>
" Misc.
  function! CMakeTargets()
      echo "Get CMake Targets"
  endfunction
" Shutdown Command
  autocmd VimLeave * :CMakeProjectTeardown
