import argparse


def get_args():

    parser = argparse.ArgumentParser("SATA_MEM_Energy_Component")

    # parser.add_argument('--ssram', type=float, default=2.750, help='dynamic energy for isram')
    # parser.add_argument('--wsram', type=float, default=6.529, help='dynamic energy for wsram')
    # parser.add_argument('--usram', type=float, default=0.239, help='dynamic energy for osram')
    # parser.add_argument('--dusram', type=float, default=0.239, help='dynamic energy for osram')
    # parser.add_argument('--zsram', type=float, default=0.239, help='dynamic energy for osram')
    # parser.add_argument('--dzsram', type=float, default=0.239, help='dynamic energy for osram')
    # parser.add_argument('--msram', type=float, default=1.176, help='dynamic energy for osram')
    parser.add_argument('--dram', type=float, default=55.58, help='dynamic energy for dram')
    parser.add_argument('--sram', type=float, default=1.95, help='dynamic energy for sram')
    parser.add_argument('--spad', type=float, default=0.2779, help='dynamic energy for spad')
    # parser.add_argument('--ispad', type=float, default=0.239, help='dynamic energy for isram')
    # parser.add_argument('--wspad', type=float, default=0.2152, help='dynamic energy for wsram')



    args = parser.parse_args()
    print(args)

    return args