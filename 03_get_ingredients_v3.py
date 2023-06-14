import pandas as pd


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


def num_check(question, error, num_type):
    valid = False

    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print()
            else:
                return response

        except ValueError:
            print(error)


# checks that string response is not blank
def not_blank(question, error):
    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print("{}. \nPlease try again\n".format(error))
            continue

        return response


# get recipe name and number of servings
recipe_name = not_blank("Enter your Recipe Name: ", "Recipe Name can't be blank")
per_serve = num_check("How many servings? ", "Please enter a number greater than 0.", int)


def get_ingredients():
    # get amount, unit, and ingredient
    ingredients_list = []
    amounts_list = []
    units_list = []

    ingredients_dict = {
        "Amount": amounts_list,
        "Unit": units_list,
        "Ingredient": ingredients_list
    }

    while True:
        ingredient = not_blank("Ingredient Name: ",
                               "The ingredient name can't be blank.")
        if ingredient.lower() == "xxx":
            # check if user entered an ingredient
            if len(ingredients_list) == 0:
                print("You cannot enter 'xxx' without entering any ingredients")
                ingredient = ""
                continue
            else:
                break

        amount = num_check("Amount (in grams, milliliters, etc.): ",
                           "Please enter a number greater than 0.", float)

        unit = not_blank("Unit of measurement: ", "The unit of measurement can't be blank.")

        ingredients_list.append(ingredient)
        amounts_list.append(amount)
        units_list.append(unit)

    # create dataframe to print
    ingredient_frame = pd.DataFrame(ingredients_dict)

    return ingredient_frame


# get the items to printing
ingredients_df = get_ingredients()

# printing area
print(f'-----{recipe_name}-----')
print(f'Servings: {per_serve}')
print("\n====== Recipe Ingredients ======")
print(ingredients_df.to_string(index=False))
