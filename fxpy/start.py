from keyboard import press
import pycountry
import sys
import pandas as pd
import os
import argparse
import importlib.metadata

# Function imports from other files
from fxpy.menu import start_menu
from fxpy.web import do_conversion

# Takes in parameter of 'sender' or 'receiver'
def get_country(country_type):
    # Final verified country variable, same variable is used as loop condition
    final_country = None
    
    while not final_country:
        #Getting input
        country = input(f"\nEnter {country_type.title()}'s country or its code: ")

        # Using fuzzy search from 'pycountry' library to get name of the country or show the user the closest matches.
        # Using try block to catch any exception if the user enter an unusual name
        try:
            fuzzy_country= pycountry.countries.search_fuzzy(country)
        except LookupError:
            print("No similar country found in the records.\nPlease try again.")
            continue
        except:
            print("An error occurred while finding the country.\nPlease try again.")
            continue

        # Trying to see if any of the results matches exactly the country name or its iso code
        # Exact matches will only be on index 0, ie, first element
        print()

        if country.lower() in (fuzzy_country[0].name.lower(), fuzzy_country[0].alpha_3.lower()):
            final_country = fuzzy_country[0]
            print(f"Selected {country_type.title()} Country: {fuzzy_country[0].name}")

        elif len(fuzzy_country) == 0:
            print(f"Could not find any country similar to: {country}.\nPlease try again.")
            continue

        else:
            print("Could not find an exact match.\nDid you mean:")
            # Everything user enters now is going to leak in the next input, therefore, I have to put in a fake input
            user_selection = start_menu(fuzzy_country)
            # Fake input and clearing it from the terminal
            input()
            sys.stdout.write(f"\033[1A")  # Moving cursor above one line
            sys.stdout.write("\033[J")  # Clear everything from the cursor down
            sys.stdout.flush()

            # User_selection is None when the user presses escape to exit to retry
            if user_selection is None:
                continue
            else:
                final_country = fuzzy_country[user_selection]
                print(f"Selected {country_type.title()} Country: {final_country.name}")

    # Some countries do not have their own currency, like Spain which uses Euro. Pycountry return None as currency for those countries and this leads to an exception.
    # For now, their is no easy solution to this problem. therefore alerting user to reenter another country
    if pycountry.currencies.get(numeric = final_country.numeric):
        return final_country
    else:
        print(f"Cannot select {final_country.name} as it does not have a currency of its own.\nPlease select the country to which the currency belongs.")
        return get_country(country_type)

# Call the get_country function to retrieve both the sender and receiver countries
def get_countries():
    
    final_sender_country = get_country('sender')

    final_receiver_country = get_country('receiver')

    return final_sender_country, final_receiver_country

# Returns country object and accepts currency object as argument
def currency_to_country(currency_code):

    try:
        currency = pycountry.currencies.get(alpha_3 = currency_code)
        return pycountry.countries.get(numeric = currency.numeric)
    except:
        print("Invalid currency code entered!\nPlease try again.")
        sys.exit()

# Prints official names of countries if any
def country_facts(countries):

    # List to collect official names, if they exist for a country
    official_names = []

    for index, country in enumerate(countries):
        if country.alpha_3 == 'USA': # Why tell someone that united states' official name is United States of America :)
            continue
        else:
            try:
                official_names.append([index, country.official_name])
            except:
                continue

    if len(official_names) == 2:
        print(f"\nDid you know?:\nThe official name of {countries[0].name} is '{official_names[0][1]}' and that of {countries[1].name} is '{official_names[1][1]}'.")
    elif len(official_names) == 1:
        print(f"\nDid you know?:\nThe official name of {countries[official_names[0][0]].name} is '{official_names[0][1]}'.")

# Entry point of the tool
def main():

    toolname = "ForexPy"

    countries = None
    # Variable to loop on to catch if the user entered the same country both the times
    are_countries_same = True

    # Parser to parse command line arguments
    parser = argparse.ArgumentParser(
        description = "A command-line tool for currency conversion that fetches live Forex exchange rates from popular exchange services using web scraping."
    )

    parser.add_argument(
        "--sender", "-s", type = str, help = "Sender Currency Alpha_3 Code"
    )

    parser.add_argument(
        "--receiver", "-r", type = str, help = "Receiver Currency Alpha_3 Code"
    )

    parser.add_argument(
        "--version", "-v", action = "version", help = "Show Version and Exit", version = f"%(prog)s {importlib.metadata.version('FxPy')}"
    )

    args = parser.parse_args()

    # Validating arguments, if any
    if args.sender and args.receiver:
        if args.sender.lower() == args.receiver.lower():
            print("Same currencies were selected for Sender and Receiver.\nPlease try again by entering different currency codes.")
            sys.exit()
        else:
            countries = [ currency_to_country(args.sender.upper()), currency_to_country(args.receiver.upper()) ]
            are_countries_same = False # Setting to false so as to prevent the while loop from asking the user for countries, when correct currency codes were entered
    elif not args.sender and not args.receiver:
        # Checking if the terminal is in admin or root mode to access keyboard functionality.
        # OS.geteuid() only returns in linux or macos. Admin mode is required for both the OSs, not for Windows.
        # Therefore, if the function returns something, then the OS being used is Linux or MacOS and root access is required. But if the funciton throws an exception, then the OS is windows and no need to check for root access.
        try:
            if os.geteuid() == 0:
                pass
            else:
                print("Terminal not in Root mode!\nPlease run the terminal as root, or use flags if you wish to run the terminal in normal mode.\nSee GitHub Repo for instructions on how to run as root or how to use flags.")
                sys.exit()
        except Exception:
            pass
    elif not args.sender or not args.receiver:
        print("\nBoth Sender and Receiver currency codes are required!\nPlease try again with valid codes for both currencies.\nNot sure what is the currency code of one of the countries? NO PROBLEM!\nJust launch the tool without any arguments and enter country names instead of currency codes.")
        sys.exit()

    # Program continues if correct currency codes were passed or no args were passed.

    print(f"Welcome to {toolname}.")

    while are_countries_same:
        # A tuple of country objects for sender and receiver countries
        countries = get_countries()

        if countries[0] is countries[1]:
            print("\nSame countries were selected for Sender and Receiver.\nPlease try again by selecting different countries.")
            continue
        else:
            are_countries_same = False

    # Converting currencies
    # List of tuples
    conversions = do_conversion(countries)

    # If the user wants the output in an excel sheet, cause why not.
    out = input("\nWould you like the output in an Excel sheet? (y or N): ")

    if out.lower() in ('y', 'yes'):
        try:
            # Makes an excel file and exports it to a file located at the current working dir
            file_path = os.path.join(os.getcwd(), f"{countries[0].name.replace(' ', '_')}_to_{countries[1].name.replace(' ', '_')}.xlsx")
            pd.DataFrame(conversions, columns = ["Service", "Conversion"]).to_excel(file_path, index = False)
            print(f"Data exported to '{file_path}'.")
        except:
            print("Could not export file. The reason may be lack of privileges.\nPlease try again with elevated terminal.")

    country_facts(countries)

    print(f"\nThanks for using {toolname}.")

if __name__ == "__main__":
    main()
