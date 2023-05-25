def dict_bubble_sort(x: dict):
    for i in range(len(x["prices"]) - 1):
        for j in range(len(x["prices"]) - i - 1):
            if x["prices"][j] > x["prices"][j + 1]:
                x["prices"][j], x["prices"][j + 1] = x["prices"][j + 1], x["prices"][j]
                x["links"][j], x["links"][j + 1] = x["links"][j + 1], x["links"][j]
    return x
