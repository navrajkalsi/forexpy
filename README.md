# ForexPy

A command-line tool for currency conversion that fetches live Forex exchange rates from popular exchange services using web scraping.

## Motivation

When sending money to another country, `how to choose which service to use?`
* You could google the conversion ,visit every site and compare the rates to find the best exchange rate

OR

* Use `ForexPy` and get rates from major services with a single command!

Personally, I was frustated whenever I needed to do a foreign transaction. If I choose one service due to its better rate next time the same service might be offering the worst rate. Therefore, I created ForexPy to save myself time, hassle and money.


## Quick Start

For `Linux & Windows`:
Install using:
* __Pypi__

__Using a virtual envrionment is recommended with `pip`__
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

In `Windows`, use the new **Windows Terminal**, preferably in Administrator mode.
**DO NOT USE STRAIGHT COMMAND PROMPT or POWERSHELL!** [Click for more details.](#windows-issue)

In `Linux` this tool requires root access (because of usage of keyboard library). Therefore, run the terminal as root OR run the command as __sudo__.
**USE 'sudo -E' TO PRESERVE ENVIRONMENT VARIABLES**. Not doing so may lead to 'Module Not Found' Error.

After Installation is complete, ForexPy can be used in the following ways:

* __With Arguments__ (No root privileges required): If you know the <a href="https://en.wikipedia.org/wiki/ISO_4217">ISO Alpha 3 Codes</a> of the currencies you want to convert, simply use the following command and pass the currency codes as arguments. The below example uses 'CAD' and 'INR'.

| Flag | Flag Description|
|:----:|:---------------:|
|-s| Sender Currency Code |
|-r| Receiver Currency Code |
|-v| Current Version of Tool |

```bash
# codes are case insensitive
fxpy --sender CAD --receiver INR
# or
fxpy -s cad -r inr
```

![CAD to INR Example Conversion](https://raw.githubusercontent.com/navrajkalsi/forexpy/refs/heads/main/media/1.gif)

* __Without Arguments__ (Root privileges may be required): If you do not know the exact currency codes, then you could just enter the following command and follow the instructions by entering in the respective country names (these names do not need to be perfect, the program will help in choosing the correct names).

```bash
fxpy
# use 'sudo -E fxpy' to preserve env vars
```

![CAD to INR Example Conversion](https://raw.githubusercontent.com/navrajkalsi/forexpy/refs/heads/main/media/2.gif)

### Windows Issue
While testing this tool on different computers, I found myself as a part of the 'works on my machine' meme:)
<br>
Context: Windows Command Prompt and Powershell do not natively support ANSI escape codes.
<br>
This program does make use of these codes when using the tool **without arguments** and selecting a country.
In such case, if the shell does not support ANSI codes you will see something similar:

![Windows Command Prompt not supporting ANSI codes](https://raw.githubusercontent.com/navrajkalsi/forexpy/refs/heads/main/media/3.png)

To resolve this use [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-US&gl=US) and use Command Prompt in this terminal.
Side Note: If you haven't already, you SHOULD try this terminal. It houses all the shells and even WSL! It looks incredible too.
