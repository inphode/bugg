import collections
import time

from .neo import neo
from .options import options

__all__ = ['logger']

class __Logger:

    def create_reset_log_history(self):
        self.max_history = options.get('max_log_history', cache=False) or None
        self.log_history = collections.deque(maxlen=self.max_history)
        # Delete and wipe buffer from memory if it exists
        if neo.vim.call('bufexists', 'bugg_buffer_log_history'):
            neo.vim.command('bwipeout bugg_buffer_log_history')
        # Create new buffer to show log history
        self.buffer_log_history = neo.vim.call('nvim_create_buf', 0, 1)
        # Set the name of the log history buffer so we can find it
        neo.vim.call('nvim_buf_set_name',
            self.buffer_log_history, 'bugg_buffer_log_history'
        )

    @property
    def log_lines(self):
        return [
            '[{}] {}'.format(log['timestamp'], log['title'])
            for log in self.log_history
        ]

    def log(self, title, details=None):
        # Add log to python log queue
        timestamp = time.strftime('%H:%M:%S')
        self.log_history.appendleft({
            'title': title,
            'timestamp': timestamp,
            'details': details,
        })

        # Add log line to top of log history buffer
        log_line = '[{}] {}'.format(timestamp, title)
        neo.vim.call('nvim_buf_set_lines',
            self.buffer_log_history, 0, 0, 0, [log_line]
        )

        if self.max_history and (len(self.log_history) >= self.max_history):
            # Delete all lines above max_history
            neo.vim.call('nvim_buf_set_lines',
                self.buffer_log_history, self.max_history, -1, 0, []
            )

logger = __Logger()
