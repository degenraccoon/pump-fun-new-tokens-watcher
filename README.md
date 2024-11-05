# Pump.fun New Token Watcher by @degenraccoon

This is a simple, free to use bot that will monitor all newly listed tokens on pump.fun, filter them as you wish and add them to a notepad watchlist.

## We also offer other ready to use bots such as, auto sinper, bump bot, volume bot for pump.fun and Solana. Contact @degenraccon on TG.

## What will you need for this script?

- Python 3.6 or higher
- `asyncio` library
- `websockets` library

You can install the required libraries using pip command in the terminal:

```
pip install asyncio websockets
```

## Configuration

Before running the script, you need to configure the following parameters at the top of the `pumpfunwatch.py` file:

```python
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
```

The bot has the following filters:
- Minimum/Maximum SOL IN BC, this filter is used to determine the minimum-maximum range of SOL in bonding curve, best used to filter out large buys at launch
- Minimum/Maximum Initial Buy, this filter is used to determine the minimum-maximum range of DEV buy at launch. 
! As an important note, this is not denominated in SOL, but in the token that was launched, 10000000 means 1%, so if you want a range between 1% and 5% it will be 10000000 and 50000000.
- Watched Traders, this filter is monitoring any DEV wallet you want, so if they launch, you will immediately know. (multiple dev wallets can be watched at the same time)
- Name Contains / Symbol Contains, this filter will search for a keyword in the Name or Symbol of the token. For example, if we use the word "cat", it will find all tokens containing this word in their name.
- Exact Names, this filter will only monitor by an exact name, if we use the word "Pepe" it will monitor the new tokens with this name, but only this name, "Pepe 2" for example will not be included, for these cases, use the filter above.


## How to use?

1. Clone this repository or download the `pumpfunwatch.py` file.
2. Configure the script by editing the parameters at the top of the file.
3. Run the script using Python:

```
python pumpfunwatch.py
```

The script will start monitoring all new launches and will write their details in a notepad called "watchlist".

## Security Notes

This script does not contain any wallet, does not cost anything to run so it's basically very safe.

## Disclaimer

This script is provided as-is, without any warranties. Use it at your own risk. Make sure you understand the implications of executing transactions on the Solana blockchain before using this script.

## License

[MIT License](LICENSE)
