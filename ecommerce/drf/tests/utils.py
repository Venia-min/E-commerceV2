class convert_to_dot_notation(dict):
    """
    Access dictionary attributes via dot notations
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
