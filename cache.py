import time

### Criando um cache próprio com timeout ###

class Cache():
    
    def __init__(self):
        self.cache = {}
        self.default_timeout = 1 # default timeout in 1 seconds
        
    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout # Using default timeout
        self.cache[key] = (value, time.time() + timeout)
        
    def get(self, key):
        try:
            value, expiration_time = self.cache[key] 
            if time.time() < expiration_time:
                return value
            else:
                del self.cache[key]
                return None
        except KeyError:
            return None
        
    def clear(self):
        self.cache = {}