from trading import get_coin_info, set_leverage, place_order_with_tp_sl
from utils import calculate_size, adjust_price_to_tick

coins = [
    {"inst_id": "BTC-USDT-SWAP", "leverage": 25, "notional": 1000, "pos_side": "long"},
    {"inst_id": "ETH-USDT-SWAP", "leverage": 25, "notional": 1000, "pos_side": "long"},
    {"inst_id": "SOL-USDT-SWAP", "leverage": 25, "notional": 1000, "pos_side": "long"},
    {"inst_id": "DOGE-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "TURBO-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "PEPE-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "WIF-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "FLOKI-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "BONK-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "MEW-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "SHIB-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    {"inst_id": "ORDI-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"}
]

for coin in coins:
    try:
        # 获取交易对相关信息
        current_price, lot_size, tick_size, max_position_limit, ct_val = get_coin_info(coin["inst_id"])
        set_leverage(coin["inst_id"], coin["leverage"], coin["pos_side"])

        # 计算下单数量
        size = calculate_size(coin["notional"], coin["leverage"], current_price, ct_val, lot_size, max_position_limit)

        # 设置不同杠杆倍数的止盈止损
        if coin["leverage"] == 10:
            tp_price = adjust_price_to_tick(current_price * 1.20, tick_size)  # 止盈 20%
            sl_price = adjust_price_to_tick(current_price * 0.94, tick_size)  # 止损 6%
        elif coin["leverage"] == 25:
            tp_price = adjust_price_to_tick(current_price * 1.10, tick_size)  # 止盈 10%
            sl_price = adjust_price_to_tick(current_price * 0.97, tick_size)  # 止损 3%
        else:
            tp_price = adjust_price_to_tick(current_price * 1.15, tick_size)  # 默认止盈 15%
            sl_price = adjust_price_to_tick(current_price * 0.95, tick_size)  # 默认止损 5%

        # 计算止盈平仓数量
        tp_size = size * 0.5  # 平掉一半仓位

        print(f"止损价格: {sl_price:.10f}")
        print(f"下单数量: {size} 合约面值: {ct_val}")
        # 执行下单
        response = place_order_with_tp_sl(coin["inst_id"], "buy", size, coin["pos_side"], tp_price, sl_price, tp_size)
        if response.get("code") == "0":
            order_data = response.get("data", [{}])[0]
            ord_id = order_data.get("ordId", "Unknown")
            s_code = order_data.get("sCode", "Unknown")
            s_msg = order_data.get("sMsg", "Unknown")

            if s_code == "0":
                print(f"{coin['inst_id']} 下单成功，订单 ID: {ord_id}")
            else:
                print(f"{coin['inst_id']} 下单部分成功，状态码: {s_code}, 消息: {s_msg}")
        else:
            print(f"{coin['inst_id']} 下单失败: {response}")
    except Exception as e:
        print(f"处理 {coin['inst_id']} 出现问题: {e}")
