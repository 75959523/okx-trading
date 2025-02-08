from trading import get_coin_info, set_leverage, place_order_with_tp_sl, place_order_for_coin
from utils import calculate_size, adjust_price_to_tick
import concurrent.futures

coins = [
    {"inst_id": "BTC-USDT-SWAP", "leverage": 30, "notional": 50, "pos_side": "long"},
    {"inst_id": "ETH-USDT-SWAP", "leverage": 30, "notional": 50, "pos_side": "long"},
    {"inst_id": "SOL-USDT-SWAP", "leverage": 30, "notional": 50, "pos_side": "long"},
    # {"inst_id": "BTC-USDT-SWAP", "leverage": 30, "notional": 50, "pos_side": "short"},
    # {"inst_id": "ETH-USDT-SWAP", "leverage": 30, "notional": 50, "pos_side": "short"},
    # {"inst_id": "SOL-USDT-SWAP", "leverage": 30, "notional": 50, "pos_side": "short"},
    # {"inst_id": "DOGE-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "TURBO-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "PEPE-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "WIF-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "FLOKI-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "BONK-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "MEW-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "SHIB-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"},
    # {"inst_id": "ORDI-USDT-SWAP", "leverage": 10, "notional": 1000, "pos_side": "long"}
]

# 批量处理多个币种
def place_orders_for_all_coins(coins):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(place_order_for_coin, coins)

# 调用批量处理
place_orders_for_all_coins(coins)