import os, sys
# Make sure we can find the bugg package in this directory
sys.path.insert(0, os.path.dirname(__file__))

import pynvim

from bugg.debugger import debugger
from bugg.options import options
from bugg.logger import logger
from bugg.neo import neo

@pynvim.plugin
class Bugg(object):

    def __init__(self, nvim):
        neo.set(nvim)
        logger.create_reset_log_history()

    @pynvim.function('BuggLogDetails', sync=True)
    def BuggLogDetails(self, args):
        # TODO: Display details in object/data explorer floating window
        pass

    @pynvim.command('BuggClearLog', nargs='*')
    def BuggClearLog(self, args):
        if len(args) > 0:
            options.set('max_log_history', int(args[0]))
        logger.create_reset_log_history()

    @pynvim.command('BuggStart')
    def BuggStart(self):
        debugger.start()

    @pynvim.command('BuggStop')
    def BuggStop(self):
        debugger.stop()

    @pynvim.command('BuggRun')
    def BuggRun(self):
        debugger.run()

    @pynvim.command('BuggSetBreakpoint', nargs='*')
    def BuggSetBreakpoint(self, args):
        buffer = neo.vim.current.buffer
        line = neo.vim.eval("line('.')")
        condition = None
        if len(args) > 0:
            condition = ' '.join(args)

        debugger.add_breakpoint(buffer, line, condition)

    @pynvim.command('BuggToggleBreakpoint')
    def BuggToggleBreakpoint(self):
        buffer = neo.vim.current.buffer
        line = neo.vim.eval("line('.')")

        debugger.toggle_breakpoint(buffer, line)
