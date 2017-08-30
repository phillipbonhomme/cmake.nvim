" Tag FZF Functions
function! s:rtags_sink(line)
  let fileLine=split(a:line, "\t")[-1]
  let filename=split(fileLine,":")[0]
  let linenumber=split(fileLine,":")[1]
  let columnnumber=split(fileLine,":")[2]
  execute "edit +" . linenumber . " " . filename
  call cursor(linenumber, columnnumber)
endfunction

function! fzf#vim#rtags(rtags_src, query, ...)
  return s:fzf('rtags', {
  \ 'source':  fzf#rtags#source(a:rtags_src),
  \ 'sink*':   s:function('s:rtags_sink'),
  \ 'options': '--exact --select-1 --exit-0 --nth 1..2 -m --tiebreak=begin --prompt "RTags> "'.s:q(a:query)}, a:000)
endfunction
