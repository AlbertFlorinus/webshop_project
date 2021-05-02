import time

def timer(func):
    def wrapper():
        before = time.time()
        func()
        print("Function took:", time.time() - before, "seconds")
    return wrapper

@timer
def adder():
    b = 0
    for i in range(1,100):
        b += b+i
    print(b)
