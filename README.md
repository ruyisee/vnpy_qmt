# vnpy_qmt
QMT Gateway for vnpy

# 实现功能
- 连接mini客户端实现普通买卖

# 安装方式
- 源码安装： 下载源码, 解压, 切换vnpy环境, 在cmd里执行
```commandline
(vnpyO) D:\work\my>cd vnpy_qmt
(vnpyO) D:\work\my\vnpy_qmt>pip install .
```
# 启用通道
1. 需要使用脚本启动方式启动vnpy, 下面是一个示例(文件名如：run.py)
2. 切换到vnpy环境(或者使用vnpy对应的python绝对路径)，运行 `python run.py`
```python

# -*- coding:utf-8 -*-

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
# 导入QMT gateway
from vnpy_qmt.qmt_gateway import QmtGateway
from vnpy_ctastrategy import CtaEngine, CtaStrategyApp


def main():
    """Start VN Trader"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_app(CtaStrategyApp)
    # 添加gateway
    main_engine.add_gateway(QmtGateway, gateway_name="QMT")

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
```



## 依赖项目
[迅投xtquant官网下载](https://dict.thinktrader.net/nativeApi/download_xtquant.html)
[迅投xtquant介绍](https://dict.thinktrader.net/nativeApi/start_now.html)
# 使用
1. 启动、登录QMT mini客户端
2. 在vn.py连接QMT
![login_qmt.png](doc%2Flogin_qmt.png)