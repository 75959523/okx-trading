from trading import place_order_for_coin
import concurrent.futures

coins = [
    {"inst_id": "BTC-USDT-SWAP", "leverage": 30, "notional": 500, "pos_side": "long"},
    {"inst_id": "SOL-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    {"inst_id": "PEPE-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},

    # {"inst_id": "ETH-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "ADA-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "SUI-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "AAVE-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "DOGE-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "SHIB-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "FLOKI-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "BONK-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
    # {"inst_id": "TURBO-USDT-SWAP", "leverage": 15, "notional": 500, "pos_side": "long"},
]

# 批量处理多个币种
def place_orders_for_all_coins(coins):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(place_order_for_coin, coins)

# 调用批量处理
place_orders_for_all_coins(coins)