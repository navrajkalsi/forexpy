# ForexPy

A command-line tool for currency conversion that fetches live Forex exchange rates from popular exchange services using web scraping.

## Motivation

When sending money to another country, `how to choose which service to use?`
* You could google the conversion ,visit every site and compare the rates to find the best exchange rate

OR

* Use `ForexPy` and get rates from major services with a single command!

Personally, I was frustated whenever I needed to do a foreign transaction. If, I choose one service due to its better rate. Next time, the same service might be offering the worst rate. Therefore, I created ForexPy to save myself time, hassle and money.


## Quick Start

Install ForexPy using:
* __Pypi__

```bash
pip install fxpy
```

* __Git__

```bash
pip install git+https://github.com/navrajkalsi/forexpy.git
```

* __Clone the Repo__

```bash
git clone https://github.com/navrajkalsi/forexpy
cd forexpy
pip install .
```

## Usage

After Installation is complete, ForexPy can be used in the following ways:

* __With Arguments__: If you know the <a href="https://en.wikipedia.org/wiki/ISO_4217">ISO Alpha 3 Codes</a> of the currencies you want to convert, simply use the following command and pass the currency codes as arguments. The below example uses 'USD' and 'INR'.

```bash
# codes are case insensitive and the flags avaliable are:
# '-s' - Sender Currency Code
# '-r' - Receiver Currency Code

fxpy --sender USD --receiver INR
# or
fxpy -s usd -r inr
```

* __Without Arguments__: If you do not know the exact currency codes, then you could just enter the following command and follow the instructions by entering in the respective country names (these names do not need to be perfect, the program will help in choosing the correct names).

```bash
fxpy
```
