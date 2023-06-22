import pandas as pd


# function to check if the input is 'yes' or 'no'
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False

    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# function to check if the input is a positive number
def num_check(question, error, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print(error)
            else:
                return response
        except ValueError:
            print(error)


# function to check if the input is not blank
def not_blank(question, error):
    while True:
        response = input(question)
        if response == "":
            print(error)
        else:
            return response


def get_ingredient_prices():
    prices_list = []
    amounts_list = []
    units_list = []
    cost_to_make = []
    
    ingredient_price_dict = {
        "Price": prices_list,
        "Amount": amounts_list,
        "Unit": units_list,
        "Cost to make": cost_to_make
    }
    # calculation depends on  what unit user typed
    
    while True:
        stop_input = yes_no("Do you want to stop entering ingredient information? (yes/no): ")
        if stop_input == "yes":
            break

        price = num_check("Price: ", "Please enter a number greater than 0.", float)
        amount = num_check("Amount (in grams, milliliters, etc.): ", "Please enter a number greater than 0.", float)
        unit = not_blank("Unit of measurement: ", "The unit of measurement can't be blank.")
        # main calculation here
        
        prices_list.append(price)
        amounts_list.append(amount)
        units_list.append(unit)

    ingredient_frame = pd.DataFrame(ingredient_price_dict)
    return ingredient_frame


ingredients_df = get_ingredient_prices()

print("\n========== Ingredient Price ==========")
print(ingredients_df.to_string(index=False))
