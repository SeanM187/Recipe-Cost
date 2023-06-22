import pandas as pd


# function to check if the input is 'yes' or 'no'
def yes_no(question):
    to_check = ["yes", "no"]
    while True:
        response = input(question).lower()
        if response in to_check:
            return response
        else:
            print("Please enter either 'yes' or 'no'.\n")


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


# get recipe name and number of servings
recipe_name = not_blank("Enter your Recipe Name: ", "Recipe Name can't be blank")
per_serve = num_check("How many servings? ", "Please enter a number greater than 0.", int)

# get amount, unit, and ingredient
ingredients = []
amounts = []
units = []

ingredients_dict = {
    "Amount": amounts,
    "Unit": units,
    "Ingredient": ingredients
}

print("\nEnter the details for each ingredient (enter 'xxx' to finish):\n")
# loop to get ingredients details
while True:
    ingredient = not_blank("Ingredient Name: ",
                           "The item name can't be blank.")
    if ingredient.lower() == "xxx":
        # check if user entered an ingredient
        if len(ingredients) == 0:
            print("You cannot enter 'xxx' without entering and ingredients")
            ingredients = ""
            continue
        else:
            break

    amount = num_check("Amount (in grams, milliliters, etc.): ", "Please enter a number greater than 0.", float)
    unit = not_blank("Unit of measurement: ", "The unit of measurement can't be blank.")

    ingredients.append(ingredient)
    amounts.append(amount)
    units.append(unit)

# create a dataFrame to display the ingredient details
df = pd.DataFrame(ingredients_dict)

# printing area
print(f'-----{recipe_name}-----')
print(f'Servings: {per_serve}')
print("\n======Recipe Ingredients======")
print(df.to_string(index=False))
