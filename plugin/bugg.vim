" Ensure this plugin can be loaded only once
if exists('g:loaded_bugg')
  finish
endif
let g:loaded_bugg = 1


" === Optional FZF support

if exists('g:bugg_enable_fzf_support')

    function! s:bugg_log_details(lines)
        call g:BuggLogDetails(a:lines)
    endfunction
    command! -bang FzfBuggLog call fzf#run({
            \ 'source': getbufline(bufnr('bugg_buffer_log_history'), 1, "$"),
            \ 'sink*': function('s:bugg_log_details'),
            \ 'window': { 'width': 0.9, 'height': 0.6 }
            \ })

endif


" === Highlight groups and signs

highlight BuggBreakpointLine guibg=#111133
highlight BuggBreakpointSign guibg=#111133 guifg=red

sign define BuggBreakpoint
        \ linehl=BuggBreakpointLine
        \ numhl=BuggBreakpointLine
        \ texthl=BuggBreakpointSign
        \ text=●>

sign define BuggBreakpointCondition
        \ linehl=BuggBreakpointLine
        \ numhl=BuggBreakpointLine
        \ texthl=BuggBreakpointSign
        \ text=●?

sign define BuggBreakpointHitCount
        \ linehl=BuggBreakpointLine
        \ numhl=BuggBreakpointLine
        \ texthl=BuggBreakpointSign
        \ text=●#


" === An optional default set of bindings

if exists('g:bugg_enable_default_bindings')

    nmap gbb :BuggToggleBreakpoint<cr>
    nmap gbB :BuggSetBreakpoint |" Leaves the cursor in command line mode for condition entry
    nmap gbl :FzfBuggLog<cr>
    nmap gbs :BuggStart<cr>
    nmap gbS :BuggStop<cr>
    nmap gbr :BuggRun<cr>

endif


" === Customisations a user of the plugin can make in their vimrc

let g:bugg_xdebug_port = 9000
let g:bugg_max_log_history = 1000
