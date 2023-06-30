import pandas as pd


# Checks that user has entered yes / no to a question
def yes_no(question):
    to_check = ["yes", "no"]

    while True:
        response = input(question).lower()
        if response in to_check:
            return response
        print("Please enter either 'yes' or 'no'.\n")


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


def get_ingredient_prices(ingredients_data, ingredient_amounts):
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
        "kg": 1000,
        "g": 1,
        "ml": 1
    }

    for i, ingredient in enumerate(ingredients_data["Ingredient"]):
        price = num_check(f"Price for {ingredient}: ", "Please enter a number greater than 0.", float)
        amount = num_check(f"Amount for {ingredient}: ", "Please enter a number greater than 0.", float)
        unit = not_blank(f"Unit of measurement for {ingredient}: ", "The unit of measurement can't be blank.")

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

# print recipe information
print(f'-----{recipe_name}-----')
print(f'Servings: {per_serve}')

# print ingredients
print("\n====== Recipe Ingredients ======")
print(ingredients_data.to_string(index=False))

# print ingredient prices
print("\n====== Ingredient Prices ======")
print(ingredient_prices_data.to_string(index=False))

# Print the total cost
print(f"\nTotal cost: ${total_cost:.2f}")

# print per serving
print(f"Per Serve: ${per_serving:.2f}")
