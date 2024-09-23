import argparse


def get_args():

    mem_dict = {}
    mem_dict['dram'] = 55.58 #! dynamic energy for dram
    mem_dict['sram'] = 1.95 #! dynamic energy for sram
    mem_dict['spad'] = 0.2779 #! dynamic energy for spad

    return mem_dict