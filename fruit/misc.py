from contextlib import contextmanager
import fcntl

@contextmanager
def lockfile(filename):
    fd = open(filename, "w")
    fcntl.flock(fd, fcntl.LOCK_EX)

    try:
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()

def add_suffix(path, suffix):
    return path.with_suffix(path.suffix + suffix)

def flatten_dict(d):
    flattened = {}

    for key,value in d.items():
        if isinstance(value, dict):
            sub_dict = flatten_dict(value)
            for k,v in sub_dict.items():
                flattened["{}-{}".format(key, k)] = v
        else:
            flattened[key] = value

    return flattened
