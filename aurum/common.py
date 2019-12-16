class SingletonMixin:
    """
        Inherit this class and make the subclass Singleton.
    """

    def __new__(cls, *args, **kwargs):
        # Store instance on cls._instance_dict with cls hash
        key = str(hash(cls))
        if not hasattr(cls, '_instance_dict'):
            cls._instance_dict = {}
        if not hasattr(cls._instance_dict, key):
            cls._instance_dict[key] = \
                super(SingletonMixin, cls).__new__(cls, *args, **kwargs)
        return cls._instance_dict[key]
