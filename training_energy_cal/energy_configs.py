import argparse


def get_args():

    parser = argparse.ArgumentParser("SATA_Energy_Component")

    parser.add_argument('--mul', type=float, default=0.239, help='dynamic energy for 16 bits multiplier')
    parser.add_argument('--acc', type=float, default=0.0389, help='dynamic energy for 16 bits accumulator')
    parser.add_argument('--add', type=float, default=0.00967, help='dynamic energy for 16 bits adder')
    parser.add_argument('--and', type=float, default=0.000794, help='dynamic energy for 16 bits bitwsie-and')
    parser.add_argument('--comp', type=float, default=0.00309, help='dynamic energy for 16 bits comparator')
    parser.add_argument('--mux', type=float, default=0.00172, help='dynamic energy for 16 bits mux with 2 inputs')
    parser.add_argument('--reg', type=float, default=0.0301, help='dynamic energy for 16 bits register')
    parser.add_argument('--sft', type=float, default=0.00605, help='dynamic energy for 16 bits sfter, 3 stage')

    # parser.add_argument('--kw', type=int, default=8, help='bitwidth for weight')
    # parser.add_argument('--ku', type=int, default=8, help='bitwidth for membrane potential')
    # parser.add_argument('--kdu', type=int, default=8, help='bitwidth for gradient of membrane potential')
    # parser.add_argument('--kds', type=int, default=8, help='bitwidth for gradient of spike')
    # parser.add_argument('--kdw', type=int, default=8, help='bitwidth for gradient of weight')
    # parser.add_argument('--kh', type=int, default=8, help='bitwidth for error')


    args = parser.parse_args()
    print(args)

    return args