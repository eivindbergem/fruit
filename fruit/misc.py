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
