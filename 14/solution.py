import math

reactions_o = {}
extra_ingredients = {}

def new_reactions():
    global extra_ingredients
    global reactions_o
    extra_ingredients = {}
    reactions_o = {}
    with open("input.txt","r") as file1:
        for line in file1:
            items = line.split(" => ")
            reactants = items[0].split(", ")
            product_data = items[1].split(" ")
            quantity_prod = int(product_data[0])
            chem_prod = product_data[1].strip()
            react_data = {}
            for reactant in reactants:
                r_data = reactant.split(" ")
                react_data[r_data[1]] = int(r_data[0])
            reaction = (quantity_prod, react_data)
            reactions_o[chem_prod] = reaction

def chemistry(chemical, n, rxns):
    needed = n
    if chemical in extra_ingredients:
        if extra_ingredients[chemical] >= n:
            extra_ingredients[chemical] -= n
            return []
        else:
            needed -= extra_ingredients[chemical]
            extra_ingredients[chemical] = 0
    multiple = math.ceil(needed / rxns[chemical][0])
    extra = multiple * rxns[chemical][0] - needed
    if chemical in extra_ingredients:
        extra_ingredients[chemical] += extra
    else:
        extra_ingredients[chemical] = extra

    ingredients = []
    for chem, num in rxns[chemical][1].items():
        ingredients.append((chem, num*multiple))
    return ingredients

def ore(n, reactions):
    for item in reactions["FUEL"][1]:
        reactions["FUEL"][1][item] *= n
    while len(reactions["FUEL"][1]) != 1 or "ORE" not in reactions["FUEL"][1]:
        new_reaction = {}
        for chemical, n in reactions["FUEL"][1].items():
            if chemical == "ORE":
                if "ORE" in new_reaction:
                    new_reaction["ORE"] += n
                else:
                    new_reaction["ORE"] = n
                continue
            new_ingredients = chemistry(chemical, n, reactions)
            for ingredient in new_ingredients:
                if ingredient[0] in new_reaction:
                    new_reaction[ingredient[0]] += ingredient[1]
                else:
                    new_reaction[ingredient[0]] = ingredient[1]
        reactions["FUEL"] = (reactions["FUEL"][0], new_reaction)
    return reactions["FUEL"][1]["ORE"]

new_reactions()
current = ore(1, reactions_o)
i = 1000000000000 // current
power = len(str(i)) - 1
i = 10 ** power
while power >= 0:
    new_reactions()
    i += 10 ** power
    current = ore(i, reactions_o)
    if current > 1000000000000:
        i -= 10 ** power
        power -= 1
print(i)