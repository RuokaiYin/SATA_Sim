import argparse

def get_energy_args():

    energy_dict = {}
    energy_dict['mul'] = 0.239 #! dynamic energy for 16 bits multiplier
    energy_dict['acc'] = 0.0389 #! dynamic energy for 16 bits accumulator
    energy_dict['add'] = 0.00967 #! dynamic energy for 16 bits adder
    energy_dict['and'] = 0.000794 #! dynamic energy for 16 bits bitwsie-and
    energy_dict['comp'] = 0.00309 #! dynamic energy for 16 bits comparator
    energy_dict['mux'] = 0.00172 #! dynamic energy for 16 bits mux with 2 inputs
    energy_dict['reg'] = 0.0301 #! dynamic energy for 16 bits register
    energy_dict['sft'] = 0.00605 #! dynamic energy for 16 bits sfter, 3 stage


    return energy_dict