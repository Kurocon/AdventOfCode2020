from days import AOCDay, day

@day(21)
class Day21(AOCDay):
    test_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".split("\n")

    ingredients = set()
    allergens = set()
    foods = []

    not_contain_allergens = None

    def common(self, input_data):
        self.ingredients = set()
        self.allergens = set()
        self.foods = []
        self.not_contain_allergens = None

        for line in input_data:
            ingredients, allergens = line.split(" (contains ")
            allergens = allergens[:-1]
            self.ingredients.update(ingredients.split(" "))
            self.allergens.update(map(lambda x: x.replace(",", ""), allergens.split(" ")))
            self.foods.append((ingredients.split(" "), list(map(lambda x: x.replace(",", ""), allergens.split(" ")))))

    def part1(self, input_data):
        not_contain_allergens = self.ingredients.copy()
        for allergen in self.allergens:
            options = None
            for f_ingredients, f_allergens in self.foods:
                if allergen in f_allergens:
                    # If the allergen is in this food too, get the intersection of the current ingredient options
                    # and the ingredients of this food.
                    if options is None:
                        options = set(f_ingredients)
                    else:
                        options = options.intersection(f_ingredients)

            if len(options) == 1:
                ingredient = options.pop()
                not_contain_allergens.discard(ingredient)

            else:
                for option in options:
                    not_contain_allergens.discard(option)

        num_times = 0
        for ingredient in not_contain_allergens:
            for f_ingredients, _ in self.foods:
                if ingredient in f_ingredients:
                    num_times += 1

        yield num_times

    def part2(self, input_data):
        allergen_map = {}
        for allergen in self.allergens:
            options = None
            for f_ingredients, f_allergens in self.foods:
                if allergen in f_allergens:
                    # If the allergen is in this food too, get the intersection of the current ingredient options
                    # and the ingredients of this food.
                    if options is None:
                        options = set(f_ingredients)
                    else:
                        options = options.intersection(f_ingredients)

            if len(options) == 1:
                ingredient = options.pop()
                allergen_map[allergen] = ingredient

            else:
                allergen_map[allergen] = options

        # If an allergen still has multiple options
        # Remove all ingredients that are already mapped to another allergen
        while any(map(lambda x: isinstance(x, set), allergen_map.values())):
            for allergen, options in allergen_map.items():
                self.debug(f"{allergen}: {options}")
                if isinstance(options, set):
                    for ingredient in allergen_map.values():
                        if isinstance(ingredient, str):
                            options.discard(ingredient)

                if len(options) == 1:
                    options = options.pop()

                allergen_map[allergen] = options

        self.debug("Done")
        canonical_list = ",".join(map(lambda x: x[1], sorted(allergen_map.items(), key=lambda x: x[0])))
        yield canonical_list
