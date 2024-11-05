import asyncio
import websockets
import json
from datetime import datetime

# Configuration constants
MINIMUM_SOL_IN_BC = None    # Set to None to disable, or number for minimum SOL in bonding curve
MAXIMUM_SOL_IN_BC = None    # Set to None to disable, or number for maximum SOL in bonding curve
MINIMUM_INITIAL_BUY = None  # Set to None to disable, or number for minimum initial token amount
MAXIMUM_INITIAL_BUY = None  # Set to None to disable, or number for maximum initial token amount
WATCHED_TRADERS = [
    # "AiCqKYqyy5fTKZk7LRV6fQJHphaTYaeZk6v37HmY9U53",  # Example trader
    # Add more trader public keys here or leave empty to disable
]
NAME_CONTAINS = [
    # "cat",  # Will match: cat, blackcat, scatter, etc.
    # Add more partial name matches here or leave empty to disable
]
SYMBOL_CONTAINS = [
    # "cat",  # Will match: CAT, CATTY, SCATS, etc.
    # Add more partial symbol matches here or leave empty to disable
]
EXACT_NAMES = [
    # "Pepe",  # Will only match "Pepe", not "Pepe2" or "PepeCoin"
    # Add more exact names here or leave empty to disable
]

# Watchlist file configuration
WATCHLIST_FILE = "watchlist.txt"

async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    
    # Create or append to watchlist file with timestamp
    with open(WATCHLIST_FILE, "a", encoding='utf-8') as f:
        f.write(f"\n\n=== New Monitoring Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    async with websockets.connect(uri) as websocket:
        # Subscribing to token creation events
        payload = {
            "method": "subscribeNewToken",
        }
        await websocket.send(json.dumps(payload))

        # Subscribing to trades made by accounts
        payload = {
            "method": "subscribeAccountTrade",
            "keys": ["AArPXm8JatJiuyEffuC1un2Sc835SULa4uQqDcaGpAjV"]  # array of accounts to watch
        }
        await websocket.send(json.dumps(payload))

        # Subscribing to trades on tokens
        payload = {
            "method": "subscribeTokenTrade",
            "keys": ["91WNez8D22NwBssQbkzjy4s2ipFrzpmn5hfvWVe2aY5p"]  # array of token CAs to watch
        }
        await websocket.send(json.dumps(payload))
        
        print(f"Monitoring for new tokens... (Saving matches to {WATCHLIST_FILE})")
        print("Filters active:")
        print(f"- SOL in bonding curve range: {MINIMUM_SOL_IN_BC if MINIMUM_SOL_IN_BC is not None else 'No min'} to {MAXIMUM_SOL_IN_BC if MAXIMUM_SOL_IN_BC is not None else 'No max'}")
        print(f"- Initial buy range: {MINIMUM_INITIAL_BUY if MINIMUM_INITIAL_BUY is not None else 'No min'} to {MAXIMUM_INITIAL_BUY if MAXIMUM_INITIAL_BUY is not None else 'No max'}")
        print(f"- Watching traders: {'Yes' if WATCHED_TRADERS else 'No'}")
        print(f"- Name contains filters: {', '.join(NAME_CONTAINS) if NAME_CONTAINS else 'None'}")
        print(f"- Symbol contains filters: {', '.join(SYMBOL_CONTAINS) if SYMBOL_CONTAINS else 'None'}")
        print(f"- Exact name filters: {', '.join(EXACT_NAMES) if EXACT_NAMES else 'None'}")
        
        async for message in websocket:
            data = json.loads(message)
            
            # Check if all required fields exist
            if not all(key in data for key in ['vSolInBondingCurve', 'initialBuy', 'traderPublicKey', 'name', 'symbol', 'mint']):
                continue

            # Check filters, using None to disable them
            min_sol_check = True if MINIMUM_SOL_IN_BC is None else data['vSolInBondingCurve'] > MINIMUM_SOL_IN_BC
            max_sol_check = True if MAXIMUM_SOL_IN_BC is None else data['vSolInBondingCurve'] < MAXIMUM_SOL_IN_BC
            min_buy_check = True if MINIMUM_INITIAL_BUY is None else data['initialBuy'] > MINIMUM_INITIAL_BUY
            max_buy_check = True if MAXIMUM_INITIAL_BUY is None else data['initialBuy'] < MAXIMUM_INITIAL_BUY
            
            # Name/symbol checks
            name_contains = not NAME_CONTAINS or any(
                filter_term.lower() in data['name'].lower() 
                for filter_term in NAME_CONTAINS
            )
            symbol_contains = not SYMBOL_CONTAINS or any(
                filter_term.lower() in data['symbol'].lower() 
                for filter_term in SYMBOL_CONTAINS
            )
            exact_name_matches = not EXACT_NAMES or data['name'] in EXACT_NAMES

            # Apply all active filters
            meets_criteria = (
                min_sol_check and
                max_sol_check and
                min_buy_check and
                max_buy_check and
                (not WATCHED_TRADERS or data['traderPublicKey'] in WATCHED_TRADERS) and
                (name_contains or symbol_contains or exact_name_matches)
            )

            if meets_criteria:
                # Console output
                print("\n=== New Token Meeting Criteria ===")
                print(f"Token Name: {data['name']}")
                print(f"Token Symbol: {data['symbol']}")
                print(f"Mint Address: {data['mint']}")
                print(f"SOL in bonding curve: {data['vSolInBondingCurve']} SOL")
                print(f"Initial token buy: {data['initialBuy']:,.2f}")
                print(f"Trader: {data['traderPublicKey']}")
                
                # Determine match type
                match_type = "Other criteria"
                if exact_name_matches and EXACT_NAMES:
                    match_type = "EXACT NAME MATCH"
                elif name_contains and NAME_CONTAINS:
                    match_type = "Name contains match"
                elif symbol_contains and SYMBOL_CONTAINS:
                    match_type = "Symbol contains match"
                
                # Save to watchlist file
                with open(WATCHLIST_FILE, "a", encoding='utf-8') as f:
                    f.write(f"\n{datetime.now().strftime('%H:%M:%S')} - {data['name']} ({data['symbol']})\n")
                    f.write(f"Mint: {data['mint']}\n")
                    f.write(f"Match type: {match_type}\n")
                    f.write(f"SOL in BC: {data['vSolInBondingCurve']}, Initial Buy: {data['initialBuy']:,.2f}\n")
                    f.write("-" * 50 + "\n")
                
                print(f"Token added to {WATCHLIST_FILE}")
                print("Full data:")
                print(json.dumps(data, indent=2))

# Run the subscribe function
if __name__ == "__main__":
    try:
        asyncio.run(subscribe())
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")