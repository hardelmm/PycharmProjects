


url = "http://192.168.3.241:8080/service/iss"
ip = url.split('/')[2].split(':')[0]
#print(ip)

case_path = "./case/case.xlsx"
case = case_path.split('/')[-1].split('.')[0]
#print(case)





def sum_data(x, y):
    return x + y

def my_data(test_data):
    def wraps(func):
        def repl(*args):
            for i in test_data:
                print('func starts')
                x, y , z = i
                func(x, y , z)
                print('func ends')
        return repl
    return wraps

@my_data([(1, 2, 3), (4,5,9)])
def test_sum_data(x, y , z):
    print("Your are verifing ({} + {}) == {}".format(x, y, z))
    assert sum_data(x, y) == z


if __name__ == "__main__":
    test_sum_data()

#这样我们在方法test_sum_data后面不加参数就可以了。
#注意：*args是可变参数的意思，
#它的实现实际上是个unpack

from functools import wraps


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)

    return with_logging


@logit
def addition_func(x,y):
    """Do some math."""
    return x + y


result = addition_func(4,5)
print(result)