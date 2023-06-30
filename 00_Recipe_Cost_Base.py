import pandas as pd


def show_instructions():
    print('''\n
***** Instructions *****
This program will ask you for...
- The name of you Recipe and how many serving
- Asks for the recipe ingredient details (name, how many, and what unit)
- Asks for each ingredients prices, how much you bought it for and what unit it is

It will then output an itemised list of the ingredients details 
with calculated cost to make for each ingredient.
It will then output the total cost of the recipe and how much per 
serving it will be.

The data will also be written to a text file which
 has the same name as your product
************************''')


def yes_no(question):
    to_check = ["yes", "no"]

    while True:
        response = input(question).lower()
        if response in to_check:
            return response
        print("Please enter either 'yes' or 'no'.\n")


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


def not_blank(question, error):
    while True:
        response = input(question)
        if response.strip() == "":
            print("{}. Please try again.\n".format(error))
        else:
            return response


def get_ingredients():
    ingredients_list = []
    amounts_list = []
    units_list = []

    ingredients_dict = {
        "Amount": amounts_list,
        "Unit": units_list,
        "Ingredient": ingredients_list
    }
    print("\nEnter the details for each ingredient (enter 'xxx' to finish):\n")
    # loop to get ingredients details
    while True:
        ingredient = not_blank("Ingredient Name: ",
                               "The ingredient name can't be blank.")
        if ingredient.lower() == "xxx":
            # check if user entered an ingredient
            if len(ingredients_list) == 0:
                print("You cannot enter 'xxx' without entering any ingredients.")
                continue
            else:
                break

        amounts = num_check("Amount (in grams, milliliters, etc.): ", "Please enter a number greater than 0.", float)
        unit = not_blank("Unit of measurement: ", "The unit of measurement can't be blank.")

        ingredients_list.append(ingredient)
        amounts_list.append(amounts)
        units_list.append(unit)

    ingredient_frame = pd.DataFrame(ingredients_dict)
    return ingredient_frame


def get_ingredient_prices(ingredients_data):
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

    conversion_factors = {
        "kg": 1000,
        "g": 1,
        "ml": 1
    }

    for ingredient in ingredients_data["Ingredient"]:
        price = num_check(f"Price for {ingredient}: ", "Please enter a number greater than 0.", float)
        amount = num_check(f"Amount for {ingredient}: ", "Please enter a number greater than 0.", float)
        unit = not_blank(f"Unit of measurement for {ingredient}: ", "The unit of measurement can't be blank.")

        prices_list.append(price)
        amounts_list.append(amount)
        units_list.append(unit)

        conversion_factor = conversion_factors.get(unit.lower(), 1)
        cost = (price / (amount * conversion_factor)) * amount
        rounded_cost = round(cost, 2)
        cost_to_make.append(rounded_cost)

    ingredient_frame = pd.DataFrame(ingredient_price_dict)
    return ingredient_frame


# ask users if they have used this program before...
want_instructions = yes_no("Have you used this program before?")

if want_instructions == "no":
    show_instructions()

# get recipe name and number of servings
recipe_name = not_blank("Enter your Recipe Name: ", "Recipe Name can't be blank")
per_serve = num_check("How many servings? ", "Please enter a number greater than 0.", int)

# get ingredients and the prices for printing
ingredients_data = get_ingredients()
ingredient_prices_data = get_ingredient_prices(ingredients_data)

# print recipe information
print(f'-----{recipe_name}-----')
print(f'Servings: {per_serve}')

# print ingredients
print("\n====== Recipe Ingredients ======")
print(ingredients_data.to_string(index=False))

# print ingredient prices
print("\n====== Ingredient Prices ======")
print(ingredient_prices_data.to_string(index=False))
