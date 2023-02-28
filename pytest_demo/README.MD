框架采用：pytest+request+allure

运行方式：
Terminal窗口，进入到testcases目录下，执行命令：

运行某一条case：pytest test_caoliao_http_post_interface.py
运行所有case: pytest
运行指定标签的case：pytest -m httptest

运行并打印过程中的详细信息：pytest -s test_caoliao_http_post_interface.py
运行并生成pytest-html报告：pytest test_caoliao_http_post_interface.py --html=../testoutput/report.html
运行并生成allure测试报告：
1. 先清除掉testoutput/result文件夹下的所有文件
2. 运行case，生成allure文件：pytest --alluredir ../testoutput/result
3. 根据文件生成allure报告：allure generate ../testoutput/result/ -o ../testoutput/report/ --clean
4. 如果不是在pycharm中打开，而是直接到report目录下打开index.html文件打开的报告无法展示数据，需要双击generateAllureReport.bat生成allure报告；