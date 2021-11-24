

def remove_numerics(string):
    return ''.join([c for c in string if not c.isnumeric()])