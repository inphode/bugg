from .breakpoint import Breakpoint
from .neo import neo
from .logger import logger
from .options import options
from .dbgp import dbgp

__all__ = ['debugger']

class __Debugger:

    def __init__(self):
        self.breakpoints = {}

    def add_breakpoint(self, buffer, line, condition=None):
        key = '{}__{}'.format(str(buffer.number), str(line))

        if key not in self.breakpoints:
            # Breakpoint does not yet exist
            self.breakpoints[key] = Breakpoint()
            self.breakpoints[key].buffer = buffer
            self.breakpoints[key].line = line
        self.breakpoints[key].condition = condition

        self.breakpoints[key].show()

    def remove_breakpoint(self, buffer, line):
        key = '{}__{}'.format(str(buffer.number), str(line))

        if key in self.breakpoints:
            self.breakpoints[key].hide()
            self.breakpoints.pop(key)

    def toggle_breakpoint(self, buffer, line):
        key = '{}__{}'.format(str(buffer.number), str(line))

        if key in self.breakpoints:
            self.remove_breakpoint(buffer, line)
        else:
            self.add_breakpoint(buffer, line)

    def start(self):
        port = options.get('xdebug_port', 9000)
        logger.log('Waiting for connection on port ' + str(port))
        neo.vim.out_write('Waiting for connection on port ' + str(port) + '\n')
        result = dbgp.listen(port)
        logger.log(result)
        neo.vim.out_write(result + '\n')

    def stop(self):
        logger.log('Closing client connection')
        neo.vim.out_write('Closing client connection\n')
        result = dbgp.close()
        logger.log(result)
        neo.vim.out_write(result + '\n')

debugger = __Debugger()
