def get_potatoes():
    return "potatoes"

if __name__ == '__main__':
    s = "trei"

    try:
        number = int(s)

    except ValueError as exc:
        print(f"something went wrong, no number: {exc}")

    a = 13
    b = 6
    print(f"{a= }, {b=}")

    lst = ["ardei", "rosii", "cartofi"]

    for veg in lst:
        for ch in veg:
            print(ch)
        print(veg)

    legume = "".join(lst)
    print(legume)

    for index, veg in enumerate(lst):
        print(lst[index])

    for i in reversed(range(2, 10, 2)):
        print(i)

    t = ("Emi", 20)

    coord = [(2, 3), (3, 3), (10, 21)]
    for _, y in coord:
        print(f"{y=}")

    stoc = {"banane": 13, "stafide": 55, "ananasi": 3}

    for fruit, nb in stoc.items():
        print(f"{fruit} = {nb} ")

    if "grape" in stoc:
        print("da avem")
    else:
        print("nu avem")

    x = 3
    if x == 20:
        y = 1
    else:
        y = 2

    y=1 if x==20 else 2

    if (veg := get_potatoes()) == "potatoes":
        print(veg)

    print([i for i in range(1,11)])
    print(sum(i for i in range(1,11)))

    name="Cristi"
    print(list(name))