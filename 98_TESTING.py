def get_ingredients():
    ingredients = {}
    while True:
        ingredient_name = input("Enter ingredient name (or 'done' to finish): ")
        if ingredient_name == "done":
            break
        cost = float(input("Enter the cost for {} (in dollars): ".format(ingredient_name)))
        ingredients[ingredient_name] = cost
    return ingredients


def main():
    ingredients = get_ingredients()
    print("\nIngredient List:")
    total_cost = 0
    for ingredient, cost in ingredients.items():
        print("{}: ${}".format(ingredient, cost))
        total_cost += cost
    print("Total cost: ${}".format(total_cost))


if __name__ == "__main__":
    main()
