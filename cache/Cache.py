class Cache:

    def __init__(self):
        self.cache = {}

    def set_cache(self, key, value):
        self.cache[key] = value

    def get_cache(self, key):
        try:
            return self.cache[key]
        except Exception as e:
            return None
    def clear(self):
        self.cache = dict()