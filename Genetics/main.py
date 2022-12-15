from random import randrange, choice


def generate():
    return [randrange(-128, 127) for _ in range(100)]


def decimal_to_binary(num):
    result = [0] * 8
    binary_num = bin(num)
    result[0] = 1 if binary_num[0] == '-' else 0
    index = -1
    while binary_num[index] != 'b':
        result[8 + index] = int(binary_num[index])
        index -= 1
    return result


def binary_to_decimal(num):
    result = 0
    for i in range(7, -1, -1):
        result += num[i] * (2 ** (7 - i))
    return result


def crossover(father, mother):
    father, mother = decimal_to_binary(father), decimal_to_binary(mother)
    result = [0] * 8
    sign = choice([0, 1])
    for i in range(8):
        if (i + sign) % 2 == 0:
            result[i] = mother[i]
        else:
            result[i] = father[i]
    return binary_to_decimal(result)


def evolution():
    current_generation = generate()
    next_generation = []
    precision = 100
    for _ in range(10000):
        best_of = [i for i in current_generation if abs(i - 2) < precision]
        while len(best_of) > 1:
            father = choice(best_of)
            best_of.remove(father)
            mother = choice(best_of)
            best_of.remove(mother)
            for _ in range(2):
                next_generation.append(crossover(father, mother))
        current_generation = next_generation.copy()
        if precision > 10:
            precision -= 0.05
        next_generation.clear()
    return current_generation


def main():
    print(evolution())


if __name__ == "__main__":
    main()
