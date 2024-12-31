def adjust_price_to_tick(price, tick_sz):
    """
    调整价格到符合 tick 精度
    """
    return round(price / tick_sz) * tick_sz

def calculate_size(notional, leverage, current_price, ct_val, lot_size, max_position_limit):
    """
    计算下单数量
    """
    total_position_value = notional * leverage
    raw_size = total_position_value / (current_price * ct_val)
    size = round(raw_size / lot_size) * lot_size
    return min(size, max_position_limit)
