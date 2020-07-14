from .neo import neo

__all__ = ['options']

class __Options:

    def __init__(self):
        self.cached_vars = {}

    def get(self, name, default=None, cache=True, prefix='bugg_'):
        name = prefix + name
        value = default

        if cache and name in self.cached_vars:
            # Return cached value
            return self.cached_vars[name]
        elif name in neo.vim.vars:
            # Return nvim value
            value = neo.vim.vars[name]

        if cache:
            # Save it for next time
            self.cached_vars[name] = value

        return value

    def set(self, name, value=None, cache=True, prefix='bugg_'):
        name = prefix + name

        # Set the value in remote nvim instance
        neo.vim.vars[name] = value

        if cache:
            # Cache it now for the next get() call
            self.cached_vars[name] = value

options = __Options()
