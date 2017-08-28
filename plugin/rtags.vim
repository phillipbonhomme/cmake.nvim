" ----------------------------------------------------------------------------
" RTags
" ----------------------------------------------------------------------------
function! s:getCurrentLocation()
    let [lnum, col] = getpos('.')[1:2]
    return printf("%s:%s:%s", expand("%"), lnum, col)
endfunction

function! s:align_lists(lists)
  let maxes = {}
  for list in a:lists
    let i = 0
    while i < len(list)
      let maxes[i] = max([get(maxes, i, 0), len(list[i])])
      let i += 1
    endwhile
  endfor
  for list in a:lists
    call map(list, "printf('%-'.maxes[v:key].'s', v:val)")
  endfor
  return a:lists
endfunction

function! s:rtags_gotodefdecl_source()
  let lines = map(split(system(
    \ 'rc --absolute-path --follow-location ' . s:getCurrentLocation()),
    \ "\n"), 'split(v:val, "\t")')
  if v:shell_error
    throw 'error from rtags client'
  endif
  return map(s:align_lists(lines), 'join(v:val, "\t")')
endfunction
function! s:rtags_findreferences_source()
  let lines = map(split(system(
    \ 'rc --absolute-path --wildcard-symbol-names --all-references --references-name ' . expand("<cword>")),
    \ "\n"), 'split(v:val, "\t")')
  if v:shell_error
    throw 'error from rtags client'
  endif
  return map(s:align_lists(lines), 'join(v:val, "\t")')
endfunction
function! s:rtags_findsymbols_source()
  let lines = map(split(system(
    \ 'rc --absolute-path --wildcard-symbol-names --find-symbols "*"'),
    \ "\n"), 'split(v:val, "\t")')
  if v:shell_error
    throw 'error from rtags client'
  endif
  return map(s:align_lists(lines), 'join(v:val, "\t")')
endfunction

function! s:rtags_sink(line)
  "execute split(a:line, "\t")[2]
  "execute "normal " . split(a:line, "\t")[0][:-1]
  call setpos("''", getpos("."))
  let fileLine=split(a:line, "\t")[0]
  let filename=split(fileLine,":")[0]
  let linenumber=split(fileLine,":")[1]
  let columnnumber=split(fileLine,":")[2]
  echo fileLine
  echo filename
  echo linenumber
  echo columnnumber
  execute "edit +" . linenumber . ":" . columnnumber. " " . filename
endfunction

function! s:rtags_gotodefdecl()
  try
    call fzf#run({'source':  s:rtags_gotodefdecl_source(),
                 \'down':    '40%',
                 \'options': '--exact --select-1 --exit-0',
                 \'sink':    function('s:rtags_sink')})
  catch
    echohl WarningMsg
    echom v:exception
    echohl None
  endtry
endfunction
function! s:rtags_findreferences()
  try
    call fzf#run({'source':  s:rtags_findreferences_source(),
                 \'down':    '40%',
                 \'options': '--exact --select-1 --exit-0',
                 \'sink':    function('s:rtags_sink')})
  catch
    echohl WarningMsg
    echom v:exception
    echohl None
  endtry
endfunction
function! s:rtags_findsymbols()
  try
    call fzf#run({'source':  s:rtags_findsymbols_source(),
                 \'down':    '40%',
                 \'options': '--exact --select-1 --exit-0',
                 \'sink':    function('s:rtags_sink')})
  catch
    echohl WarningMsg
    echom v:exception
    echohl None
  endtry
endfunction

command! RTagsGoTo call s:rtags_gotodefdecl()
command! RTagsFindRefs call s:rtags_findreferences()
command! RTagsFindSymbol call s:rtags_findsymbols()
