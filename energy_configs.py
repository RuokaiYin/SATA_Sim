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

    args = parser.parse_args()
    print(args)

    return args