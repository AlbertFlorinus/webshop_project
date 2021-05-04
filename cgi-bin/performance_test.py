import time

def timer(func):
    def wrapper(*args):
        before = time.time()
        func(*args)
        print("Function took:", time.time() - before, "seconds")
    return wrapper

