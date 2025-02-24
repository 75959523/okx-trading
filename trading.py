from api_client import send_request
from utils import calculate_size, adjust_price_to_tick

# 计算止损价格的通用逻辑
def calculate_stop_loss_price(pos_side, leverage, current_price, tick_size):
    if pos_side == "long":
        # 做多时的止损价格（市场下跌）
        if leverage == 10:
            return adjust_price_to_tick(current_price * 0.925, tick_size)  # 下跌7.5% 止损
        elif leverage == 15:
            return adjust_price_to_tick(current_price * 0.955, tick_size)  # 下跌4.5% 止损
        elif leverage == 20:
            return adjust_price_to_tick(current_price * 0.96, tick_size)  # 下跌4% 止损
        elif leverage == 25:
            return adjust_price_to_tick(current_price * 0.97, tick_size)  # 下跌3% 止损
        elif leverage == 30:
            return adjust_price_to_tick(current_price * 0.975, tick_size)  # 下跌2.5% 止损
        else:
            return adjust_price_to_tick(current_price * 0.95, tick_size)  # 默认下跌5% 止损
    elif pos_side == "short":
        # 做空时的止损价格（市场上涨）
        if leverage == 10:
            return adjust_price_to_tick(current_price * 1.075, tick_size)  # 上涨7.5% 止损
        elif leverage == 15:
            return adjust_price_to_tick(current_price * 1.045, tick_size)  # 上涨4.5% 止损
        elif leverage == 20:
            return adjust_price_to_tick(current_price * 1.04, tick_size)  # 上涨4% 止损
        elif leverage == 25:
            return adjust_price_to_tick(current_price * 1.03, tick_size)  # 上涨3% 止损
        elif leverage == 30:
            return adjust_price_to_tick(current_price * 1.025, tick_size)  # 上涨2.5% 止损
        else:
            return adjust_price_to_tick(current_price * 1.05, tick_size)  # 默认上涨5% 止损

def place_order_for_coin(coin):
    try:
        # 获取交易对相关信息
        current_price, lot_size, tick_size, max_position_limit, ct_val = get_coin_info(coin["inst_id"])

        # 计算下单数量
        size = calculate_size(coin["notional"], coin["leverage"], current_price, ct_val, lot_size, max_position_limit)

        # 计算止损价格
        sl_price = calculate_stop_loss_price(coin["pos_side"], coin["leverage"], current_price, tick_size)

        # 设置杠杆倍数
        set_leverage(coin["inst_id"], coin["leverage"], coin["pos_side"])

        # 执行下单
        side = "buy" if coin["pos_side"] == "long" else "sell"
        response = place_order_with_tp_sl(coin["inst_id"], side, size, coin["pos_side"], None, sl_price, None)

        # 检查响应
        if response and response.get("code") == "0":
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

def get_coin_info(inst_id):
    """
    获取交易对的所有关键信息（市场价格、最小下单单位、最大持仓限额、合约面值）
    """
    current_price = get_market_price(inst_id)
    lot_size, tick_size, max_position_limit, ct_val = get_instrument_details(inst_id)
    formatted_price = f"{current_price:.10f}"
    print(f"{inst_id} 开仓价格: {formatted_price}")
    return current_price, lot_size, tick_size, max_position_limit, ct_val

def get_market_price(inst_id):
    request_path = f'/api/v5/market/ticker?instId={inst_id}'
    status_code, response = send_request('GET', request_path)
    if status_code == 200:
        return float(response['data'][0]['last'])
    else:
        raise Exception(f"获取市场价格失败: {response}")

def get_instrument_details(inst_id):
    request_path = f'/api/v5/public/instruments?instType=SWAP&instId={inst_id}'
    status_code, response = send_request('GET', request_path)
    if status_code == 200 and response['data']:
        data = response['data'][0]
        lot_size = float(data['lotSz'])
        tick_size = float(data['tickSz'])
        max_position_limit = int(data.get('maxLmtSz', 0))
        ct_val = float(data['ctVal'])
        return lot_size, tick_size, max_position_limit, ct_val
    else:
        raise Exception(f"获取交易对详情失败: {response}")

def set_leverage(inst_id, lever, pos_side):
    request_path = '/api/v5/account/set-leverage'
    body = {
        "instId": inst_id,
        "lever": str(lever),
        "mgnMode": "isolated",
        "posSide": pos_side
    }
    status_code, response = send_request('POST', request_path, body)
    if status_code == 200 and response['code'] == '0':
        print(f"杠杆倍数: {lever}x")
        print(f"方向: {pos_side}")
        return response
    else:
        raise Exception(f"杠杆设置失败: {response}")

def place_order_with_tp_sl(inst_id, side, size, pos_side, tp_price=None, sl_price=None, tp_size=None):
    body = {
        "instId": inst_id,
        "tdMode": "isolated",
        "side": side,
        "ordType": "market",
        "sz": f"{size:.6f}",
        "posSide": pos_side,
    }
    if tp_price:
        body["tpTriggerPx"] = f"{tp_price:.10f}"
        body["tpOrdPx"] = "-1"
        body["tpSz"] = f"{tp_size:.6f}"
    if sl_price:
        body["slTriggerPx"] = f"{sl_price:.10f}"
        body["slOrdPx"] = "-1"
    status_code, response = send_request('POST', '/api/v5/trade/order', body)
    return response
