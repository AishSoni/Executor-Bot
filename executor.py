from binance.client import Client
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

load_dotenv()
client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

# Logging setup
LOG_FILE = "logs/trade_log.csv"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(message)s')

def is_valid_tp_sl(position, entries, targets, stop_loss):
    avg_entry = sum(entries) / len(entries)
    if position == "long":
        return all(tp > avg_entry for tp in targets) and stop_loss < avg_entry
    if position == "short":
        return all(tp < avg_entry for tp in targets) and stop_loss > avg_entry
    return False

def place_trade(signal, presets):
    # leverage logic
    levs = [int(x) for x in signal["leverage"].replace("x", "").split("-")]
    effective_leverage = min(min(levs), presets["max_leverage"])

    entries = list(map(float, signal["entries"]))
    targets = list(map(float, signal["targets"]))
    stop_loss = float(signal["stop_loss"])
    position = signal["position"]
    symbol = signal["symbol"].upper()
    
    if not is_valid_tp_sl(position, entries, targets, stop_loss):
        raise ValueError("Invalid TP/SL relative to entry and position type")

    avg_entry = sum(entries) / len(entries)
    margin_per_target = presets["risk_amount"] / len(targets)
    qty_per_target = (margin_per_target * effective_leverage) / avg_entry

    # Place single order for now (simplified)
    side = Client.SIDE_BUY if position == "long" else Client.SIDE_SELL

    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=round(qty_per_target, 1),
    )

    log = f"{datetime.now()},{symbol},{position},{avg_entry},{stop_loss},{targets},{effective_leverage},{qty_per_target}"
    print(log)
    logging.info(log)
