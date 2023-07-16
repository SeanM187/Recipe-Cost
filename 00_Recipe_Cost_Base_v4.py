import pandas as pd
from datetime import date


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


# Checks that user has entered yes / no to a question
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


# checks that input is either a float or an
# integer that is more than zero. Takes in custom error message
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


# checks that user entered something
def not_blank(question, error):
    while True:
        response = input(question)
        if response.strip() == "":
            print("{}. Please try again.\n".format(error))
        else:
            return response


# gets all the ingredients name amount and unit
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

        amounts = num_check("Amount needed for the recipe (in grams, milliliters, etc.): ",
                            "Please enter a number greater than 0.", float)
        unit = not_blank("Unit of measurement: ", "The unit of measurement can't be blank.")

        ingredients_list.append(ingredient)
        amounts_list.append(amounts)
        units_list.append(unit)

    ingredient_frame = pd.DataFrame(ingredients_dict)
    return ingredient_frame


# gets each of the ingredients prices, amounts bought, units, and prints the cost to make
def get_ingredient_prices(ingredients_name, ingredient_amounts):
    prices_list = []
    amounts_list = []
    units_list = []
    cost_to_make = []
    unrounded_cost_total = 0

    ingredient_price_dict = {
        "Price": prices_list,
        "Amount": amounts_list,
        "Unit": units_list,
        "Cost to make": cost_to_make,
    }

    conversion_factors = {
        "kg": 1,
        "g": 1,
        "ml": 1
    }
    
    # gets each of the individual ingredients price, amounts, and units
    for i, ingredient in enumerate(ingredients_name["Ingredient"]):
        price = num_check(f"Price for {ingredient}: $", "Please enter a number greater than 0.", float)
        amount = num_check(f"Amount for {ingredient}: ", "Please enter a number greater than 0.", float)
        # I decided to make it only accepts kg,g or ml for this function and can be added more units
        while True:
            unit = not_blank(f"Unit of measurement for {ingredient}: ", "The unit of measurement can't be blank.").lower()
            if unit in ["kg", "g", "ml"]:
                break
            else:
                print("Invalid unit of measurement. Please enter either 'kg', 'g', or 'ml'.\n")

        prices_list.append(price)
        amounts_list.append(amount)
        units_list.append(unit)

        conversion_factor = conversion_factors.get(unit.lower(), 1)
        cost = price / (amount * conversion_factor) * ingredient_amounts[i]
        unrounded_cost_total += cost
        rounded_cost = round(cost, 2)
        cost_to_make.append(rounded_cost)

    ingredient_frame = pd.DataFrame(ingredient_price_dict)
    return ingredient_frame, unrounded_cost_total


# ask users if they have used this program before
want_instructions = yes_no("Have you used this program before?")

if want_instructions == "no":
    show_instructions()

# get recipe name and number of servings
recipe_name = not_blank("Enter your Recipe Name: ", "Recipe Name can't be blank")
per_serve = num_check("How many servings? ", "Please enter a number greater than 0.", int)

# get ingredients and the prices for printing
ingredients_data = get_ingredients()
ingredient_prices_data, unrounded_total_cost = get_ingredient_prices(ingredients_data, ingredients_data["Amount"])

# Calculate total cost
total_cost = unrounded_total_cost

# Calculate per serving
per_serving = total_cost / per_serve

# create the date
today = date.today()

day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%y")

# file name
file_name = f"{recipe_name}_{day}_{month}_{year}"

# strings for printing / export
recipe_name_txt = f"***** {recipe_name} - {day}/{month}/{year} *****"
per_serve_txt = f"Per Serving: {per_serve}"
ingredients_heading_txt = f"\n----- Recipe Ingredients -----"
recipe_ingredients_txt = ingredients_data.to_string(index=False)
ingredient_prices_heading_txt = f"\n----- Ingredient Price -----"
ingredient_price_txt = ingredient_prices_data.to_string(index=False)
total_cost_txt = f"\nTotal Cost: ${total_cost:.2f}"
per_serving_txt = f"Per Serve: ${per_serving:.2f}"

# list to hold all strings for printing
to_write = [recipe_name_txt, per_serve_txt, ingredients_heading_txt,
            recipe_ingredients_txt, ingredient_prices_heading_txt, ingredient_price_txt,
            total_cost_txt, per_serving_txt]

# write to file
write_to = "{}.txt".format(file_name)
text_file = open(write_to, "w+")

# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n")

# close file
text_file.close()

# print stuff
for item in to_write:
    print(item)
    print()
