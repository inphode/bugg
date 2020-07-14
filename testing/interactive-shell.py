import code
import neovim
import os
import readline
import rlcompleter

nvim = neovim.attach('socket', path=os.environ['NVIM_LISTEN_ADDRESS'])

def create_bugg():
    from plugin import plugin
    return plugin.Bugg(nvim)

readline.parse_and_bind("tab: complete")
code.interact(local=locals())
