import logging
import allure

import pytest
from utils.http_utils import HttpUtils
from utils.read_jsonfile_utils import ReadJsonFileUtils
from config.global_config import CAOLIAO_HTTP_GET_HOST


@pytest.mark.httptest
@allure.feature("草料二维码get请求测试")
class TestHttpInterface:
    # 获取文件相对路径
    data_file_path = ReadJsonFileUtils.get_data_path("resources", "test_http_get_data.json")
    # 读取测试数据文件
    param_data = ReadJsonFileUtils(data_file_path)
    data_item = param_data.get_value('dataItem')  # 是一个list列表，list列表中包含多个字典

    """
    @pytest.mark.parametrize是数据驱动;
    data_item列表中有几个字典，就运行几次case
    ids是用于自定义用例的名称

    """

    @pytest.mark.parametrize("args", data_item, ids=['测试草料二维码get接口1', '测试草料二维码get接口2'])
    def test_caoliao_get_demo(self, args, login_test):
        # 打印用例ID和名称到报告中显示
        print("用例ID:{}".format(args['id']))
        print("用例名称:{}".format(args['name']))
        print("测试conftest传值：{}".format(login_test))
        logging.info("测试开始啦~~~~~~~")
        res = HttpUtils.http_get(args['headers'], CAOLIAO_HTTP_GET_HOST+args['url'])
        # assert断言，判断接口是否返回期望的结果数据
        assert str(res.get('code')) == str(args['expectdata']['code']), "接口返回status值不等于预期"


# if __name__ == '__main__':
#     TestHttpInterface().test_http_get_001()
#     # TestHttpInterface().test_http_post_001()
