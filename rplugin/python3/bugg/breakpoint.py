from .neo import neo
from .logger import logger

class Breakpoint:

    def __init__(self):
        self.buffer = None
        self.line = None
        self.file = None
        self.condition = None
        self.identifier = None

    def show(self):
        if self.identifier:
            self.hide()

        # Store the full path to the file
        self.file = neo.vim.call('expand',
            '#{}:p'.format(str(neo.vim.current.buffer.number))
        )

        log_line = 'Setting breakpoint on line {} of buffer {}'.format(
            str(self.line), str(self.buffer.name or self.buffer.number)
        )

        if self.condition:
            log_line += ' with condition ' + str(self.condition)
            sign = 'BuggBreakpointCondition'
        else:
            sign = 'BuggBreakpoint'

        logger.log(log_line)

        # Place the breakpoint sign at the line in the buffer
        self.identifier = neo.vim.call('sign_place',
            0, 'BuggBreakpoint', sign, self.buffer, {'lnum': self.line, 'priority': 1}
        )

        logger.log('Breakpoint set with sign ID: ' + str(self.identifier))

    def hide(self):
        log_line = 'Removing breakpoint on line {} of buffer {}'.format(
            str(self.line), str(self.buffer.name or self.buffer.number)
        )
        logger.log(log_line)

        if self.identifier:
            # Remove the breakpoint sign
            neo.vim.call('sign_unplace',
                'BuggBreakpoint', {'buffer': self.buffer, 'id': self.identifier}
            )

        logger.log('Breakpoint removed with sign ID: ' + str(self.identifier))
