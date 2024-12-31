from api_client import send_request

def get_coin_info(inst_id):
    """
    获取交易对的所有关键信息（市场价格、最小下单单位、最大持仓限额、合约面值）
    """
    current_price = get_market_price(inst_id)
    lot_size, tick_size = get_instrument_details(inst_id)
    max_position_limit, ct_val = get_max_position_limit(inst_id)
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
        return float(response['data'][0]['lotSz']), float(response['data'][0]['tickSz'])
    else:
        raise Exception(f"获取交易对详情失败: {response}")

def get_max_position_limit(inst_id):
    request_path = f'/api/v5/public/instruments?instType=SWAP&instId={inst_id}'
    status_code, response = send_request('GET', request_path)
    if status_code == 200 and response['data']:
        data = response['data'][0]
        return int(data.get('maxLmtSz', 0)), float(data['ctVal'])
    else:
        raise Exception(f"获取最大持仓限额失败: {response}")

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
