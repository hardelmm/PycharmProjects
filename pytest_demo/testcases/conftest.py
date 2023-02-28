import logging
import traceback

import pytest
import requests

"""
如果用例执行前需要先登录获取token值，就要用到conftest.py文件了
作用：conftest.py 配置里可以实现数据共享，不需要import导入 conftest.py，pytest用例会自动查找
scope参数为session，那么所有的测试文件执行前执行一次
scope参数为module，那么每一个测试文件执行前都会执行一次conftest文件中的fixture
scope参数为class，那么每一个测试文件中的测试类执行前都会执行一次conftest文件中的fixture
scope参数为function，那么所有文件的测试用例执行前都会执行一次conftest文件中的fixture

"""

# 获取到登录请求返回的ticket值，@pytest.fixture装饰后，testcase文件中直接使用函数名"login_ticket"即可得到ticket值
@pytest.fixture(scope="session")
def login_ticket():
    header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    params = {
        "loginId": "username",
        "pwd": "password",
    }
    url = 'http://testxxxxx.xx.com/doLogin'
    logging.info('开始调用登录接口:{}'.format(url))
    res = requests.post(url, data=params, headers=header, verify=False)  # verify：忽略https的认证
    try:
        ticket = res.headers['Set-Cookie']
    except Exception as ex:
        logging.error('登录失败！接口返回：{}'.format(res.text))
        traceback.print_tb(ex)
    logging.info('登录成功，ticket值为：{}'.format(ticket))
    return ticket

#测试一下conftest.py文件和fixture的作用
@pytest.fixture(scope="session")
def login_test():
    print("运行用例前先登录！")

    # 使用yield关键字实现后置操作，如果上面的前置操作要返回值，在yield后面加上要返回的值
    # 也就是yield既可以实现后置，又可以起到return返回值的作用
    yield "runBeforeTestCase"
    print("运行用例后退出登录！")
