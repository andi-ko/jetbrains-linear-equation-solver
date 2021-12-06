import sys, getopt


def parse_infile(infile):
    with open(infile) as f:
        lines = f.readlines()
        matrix = []
        for line in lines[1:]:
            matrix.append(list(map(lambda _x: float(_x), line.split())))
        return matrix
    return None


def parse_matrix(matrix):

    for idx, equation in enumerate(matrix):
        # get nonzero element at current column index
        shift = 1
        while equation[idx] == 0:
            temp = matrix[idx]
            matrix[idx] = matrix[idx + shift]
            matrix[idx + shift] = temp
            shift += 1

        # divide by current coefficient
        matrix[idx] = list(map(lambda _x: _x / equation[idx], equation))

        # zero all further elements in current column
        for idx2, equation2 in enumerate(matrix[idx + 1:]):
            factor = equation2[idx] / equation[idx]
            matrix[idx + 1 + idx2] = \
                list(map(lambda _x, _y: _x - _y * factor, equation2, equation))

    # zero rows in reverse direction
    matrix.reverse()
    for idx, equation in enumerate(matrix, 1):
        equation.reverse()
        for idx2, equation2 in enumerate(matrix[idx:]):
            equation2.reverse()
            factor = equation2[idx] / equation[idx]
            matrix[idx + idx2] = \
                list(map(lambda _x, _y: _x - _y * factor, equation2, equation))
            matrix[idx + idx2].reverse()
        equation.reverse()
    matrix.reverse()
    return [equation[len(equation) - 1] for equation in matrix]


def write_outfile(outfile, coefficients):
    with open(outfile, "w") as f:
        f.writelines(list(map(lambda _x: str(_x) + '\n', coefficients)))


def main(argv):
    infile = ''
    outfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["infile=", "outfile="])
    except getopt.GetoptError:
        print('test.py -i <infile> -o <outfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <infile> -o <outfile>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg
    matrix = parse_infile(infile)
    coefficients = parse_matrix(matrix)
    write_outfile(outfile, coefficients)


if __name__ == "__main__":
    main(sys.argv[1:])
