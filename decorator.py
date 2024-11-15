def decorator(func):
    def wraps(*args, **kwargs):
        print("-----")
        func(*args, **kwargs)
        print('--------')
        return
    return wraps


@decorator
def my_print(name):
    print(f'hello, {name}')

@decorator
def my_print1(name):
    print(f'hello, {name}')

@decorator
def my_print2(name, a):
    print(f'hello, {name}, {a}')


my_print('Ivan')
my_print1('Pasha')
my_print2('Dima', 2)
