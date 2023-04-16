# Stock Trade Simulator

This is a Python program that simulates stock trades based on a given strategy. It uses the *yfinance* module to download stock data.

## Requirements
* Python 3.9.7
* The rest of the packages can be installed using 
  <code bash>
  pip install -r requirements.txt
  </code>
## Installation

1. Clone this repository:

```bash=
git clone git@github.com:jpjp927/stock-trade-simulator.git
cd stock-trade-simulator
```

2. Install required module:

```bash=
pip install yfinance
```

## Usage

To run the simulator, execute the `main.py` file with the desired arguments:

```
python main.py 
```

This will simulate a pullback trading strategy with NVDA stock data from 2020-01-01 to 2022-03-02, starting with an initial capital of $10,000 and a pullback threshold of 1%.

You can also modify the code to use a different strategy or stock data by editing the `simulate` method and the variables at the end of the code.

## Contributing

If you find any bugs or have suggestions for improvement, please create an issue or a pull request. We welcome any contributions that can make this program better!

## License

This program is licensed under the MIT License. See the LICENSE file for details.
