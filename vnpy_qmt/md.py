# -*- coding:utf-8 -*-
"""
@FileName  :md.py
@Time      :2022/11/8 17:14
@Author    :fsksf
"""

from vnpy.trader.object import (
    CancelRequest, OrderRequest, SubscribeRequest, TickData,
    ContractData
)
import xtquant.xtdata
import xtquant.xttrader
import xtquant.xttype
from vnpy_qmt.utils import (
    From_VN_Exchange_map, TO_VN_Exchange_map, to_vn_contract,
    TO_VN_Product, to_vn_product, timestamp_to_datetime,
    to_qmt_code
)


class MD:

    def __init__(self, gateway):
        self.gateway = gateway
        self.th = None
        self.limit_ups = {}
        self.limit_downs = {}

    def close(self) -> None:
        pass

    def subscribe(self, req: SubscribeRequest) -> None:

        return xtquant.xtdata.subscribe_quote(
            stock_code=f'{req.symbol}.{From_VN_Exchange_map[req.exchange]}',
            period='tick',
            callback=self.on_tick
        )

    def connect(self, setting: dict) -> None:
        self.get_contract()
        return

    def get_contract(self):
        self.write_log('开始获取标的信息')
        contract_ids = set()
        bk = ['上期所', '上证A股', '上证B股', '中金所', '创业板', '大商所',
              '沪市ETF', '沪市指数', '沪深A股',
              '沪深B股', '沪深ETF', '沪深指数', '深市ETF',
              '深市基金', '深市指数', '深证A股', '深证B股', '科创板', '科创板CDR',
              ]
        for sector in bk:
            print(sector)
            stock_list = xtquant.xtdata.get_stock_list_in_sector(sector_name=sector)
            for symbol in stock_list:
                if symbol in contract_ids:
                    continue
                contract_ids.add(symbol)
                info = xtquant.xtdata.get_instrument_detail(symbol)
                contract_type = xtquant.xtdata.get_instrument_type(symbol)
                if info is None or contract_type is None:
                    continue
                try:
                    exchange = TO_VN_Exchange_map[info['ExchangeID']]
                except KeyError:
                    print('本gateway不支持的标的', symbol)
                    continue
                if exchange not in self.gateway.exchanges:
                    continue
                product = to_vn_product(contract_type)
                if product not in self.gateway.TRADE_TYPE:
                    continue

                c = ContractData(
                    gateway_name=self.gateway.gateway_name,
                    symbol=info['InstrumentID'],
                    exchange=exchange,
                    name=info['InstrumentName'],
                    product=product,
                    pricetick=info['PriceTick'],
                    size=100,
                    min_volume=100
                )
                self.limit_ups[c.vt_symbol] = info['UpStopPrice']
                self.limit_downs[c.vt_symbol] = info['DownStopPrice']
                self.gateway.on_contract(c)
        self.write_log('获取标的信息完成')

    def on_tick(self, datas):
        for code, data_list in datas.items():
            symbol, suffix = code.rsplit('.')
            exchange = TO_VN_Exchange_map[suffix]
            for data in data_list:
                ask_price = data['askPrice']
                ask_vol = data['askVol']
                bid_price = data['bidPrice']
                bid_vol = data['bidVol']

                tick = TickData(
                    gateway_name=self.gateway.gateway_name,
                    symbol=symbol,
                    exchange=exchange,
                    datetime=timestamp_to_datetime(data['time']),
                    last_price=data['lastPrice'],
                    volume=data['volume'],
                    open_price=data['open'],
                    high_price=data['high'],
                    low_price=data['low'],
                    pre_close=data['lastClose'],
                    limit_down=0,
                    limit_up=0,
                    ask_price_1=ask_price[0],
                    ask_price_2=ask_price[1],
                    ask_price_3=ask_price[2],
                    ask_price_4=ask_price[3],
                    ask_price_5=ask_price[4],

                    ask_volume_1=ask_vol[0],
                    ask_volume_2=ask_vol[1],
                    ask_volume_3=ask_vol[2],
                    ask_volume_4=ask_vol[3],
                    ask_volume_5=ask_vol[4],

                    bid_price_1=bid_price[0],
                    bid_price_2=bid_price[1],
                    bid_price_3=bid_price[2],
                    bid_price_4=bid_price[3],
                    bid_price_5=bid_price[4],

                    bid_volume_1=bid_vol[0],
                    bid_volume_2=bid_vol[1],
                    bid_volume_3=bid_vol[2],
                    bid_volume_4=bid_vol[3],
                    bid_volume_5=bid_vol[4],
                )
                contract = self.gateway.get_contract(tick.vt_symbol)
                if contract:
                    tick.name = contract.name
                tick.limit_up = self.limit_ups.get(tick.vt_symbol, None)
                tick.limit_down = self.limit_downs.get(tick.vt_symbol, None)
                self.gateway.on_tick(tick)
    def write_log(self, msg):
        self.gateway.write_log(f"[ md ] {msg}")