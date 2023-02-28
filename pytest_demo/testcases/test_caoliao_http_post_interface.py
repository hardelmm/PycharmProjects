import pytest
import logging
import allure
from utils.http_utils import HttpUtils
from utils.read_jsonfile_utils import ReadJsonFileUtils
from config.global_config import CAOLIAO_HTTP_POST_HOST

"""
运行：pytest test_caoliao_http_post_interface.py
运行并打印过程中的详细信息：pytest -s test_caoliao_http_post_interface.py
运行并生成pytest-html报告：pytest test_caoliao_http_post_interface.py --html=../testoutput/report.html
运行并生成allure测试报告：
1. pytest --alluredir ../testoutput/result
2. allure generate ../testoutput/result/ -o ../testoutput/report/ --clean
3. 直接到report目录下打开index.html文件打开的报告无法展示数据，需要双击generateAllureReport.bat生成allure报告；


"""


# pytest.ini文件中要添加markers = httptest，不然会有warning，说这个Mark有问题
@pytest.mark.httptest
@allure.feature("草料二维码post请求测试")
class TestHttpInterface:
    # 获取文件相对路径
    data_file_path = ReadJsonFileUtils.get_data_path("resources", "test_http_post_data.json")
    # 读取测试数据文件
    param_data = ReadJsonFileUtils(data_file_path)
    data_item = param_data.get_value('dataItem') #是一个list列表，list列表中包含多个字典

    """
    @pytest.mark.parametrize是数据驱动;
    data_item列表中有几个字典，就运行几次case
    ids是用于自定义用例的名称
    
    """
    @pytest.mark.parametrize("args", data_item, ids=['测试草料二维码post接口1','测试草料二维码post接口2'])
    def test_caoliao_post_demo(self, args):
        # 打印用例ID和名称到报告中显示
        print("用例ID:{}".format(args['id']))
        print("用例名称:{}".format(args['name']))
        logging.info("测试开始啦~~~~~~~")
        res = HttpUtils.http_post(args['headers'], CAOLIAO_HTTP_POST_HOST+args['url'], args['parameters'])
        # assert断言，判断接口是否返回期望的结果数据
        assert str(res.get('status')) == str(args['expectdata']['status']), "接口返回status值不等于预期"
        assert str(res.get('data').get('qrtype')) == str(args['expectdata']['qrtype']), "接口返回qrtype值不等于预期"

