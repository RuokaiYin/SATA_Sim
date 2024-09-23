import argparse
import energy_configs
import mem_configs
import yaml
from get_workload import get_workload
from get_arch_energy import get_arch_energy


def main():
    #! parser for the command line arguments
    parser = argparse.ArgumentParser(description='main simulation script for HAR-SNN')
    parser.add_argument('--fwdb', default=8, type=int, help='Bitwidth for fwd (weight or ANN\'s activation)')
    parser.add_argument('--sps', default=0.9, type=float, help='Activation Sparsity')
    parser.add_argument('--network', default='dcl', type=str, help='model types: [dcl, sdcl, fcn, sfcn]')
    args = parser.parse_args()
    network_type = args.network

    #! Model naming with the s in the beginning is for the spiking version of the model
    if network_type == 'dcl':
        hw_config = './hw_configs/sata_ann_watch_config.yaml'
        network_path = './har_configs/dcl_har.yaml'
    elif network_type == 'sdcl':
        hw_config = './hw_configs/sata_watch_config.yaml'
        network_path = './har_configs/dcl_shar.yaml'
    elif network_type == 'fcn':
        hw_config = './hw_configs/sata_ann_watch_config.yaml'
        network_path = './har_configs/fcn_har.yaml'
    elif network_type == 'sfcn':
        hw_config = './hw_configs/sata_watch_config.yaml'
        network_path = './har_configs/fcn_shar.yaml'

    #! Those are actually the dictionaries for the energy and memory arguments
    energy_args = energy_configs.get_energy_args()
    mem_args = mem_configs.get_args()

    #! IMPORTANT: For HAR simulation, please set T = 1 for all experiments.
    T = 1
    fwd_b = args.fwdb
    sp_s = args.sps

    #! Currently only support the forward pass for computation energy
    keyword = ['act','mac_fwd']

    #? Both dictionaries have (act: value) and (mac_fwd: value)
    workload_d = get_workload(T,fwd_b,network_path,sp_s)
    arch_d = get_arch_energy(energy_args, mem_args, hw_config, fwd_b)

  
    total_energy = 0
    total_fwd_comp_act = 0
    total_fwd_comp_mac = 0
    #TODO: to be implemented
    total_fwd_mem = 0

    for k in keyword:
        total_energy += workload_d[k] * arch_d[k]

        if 'act' in k:
            total_fwd_comp_act += workload_d[k]*arch_d[k]
        elif 'mac_fwd' in k:
            total_fwd_comp_mac += workload_d[k]*arch_d[k]


    single_ann_mac = 0.239 + 0.0389 #! This value is the hardcoded energy for one ANN MAC operation (16-bits)
    print("Bitwidth for fwd (weight or ANN's activation): ", fwd_b)
    print("Total Inference Energy in (\MAC(16-bit)): ", total_energy/single_ann_mac)
    print("Total Fwd Energy (act) in (\MAC(16-bit)): ", total_fwd_comp_act/single_ann_mac)  
    print("Total Fwd Energy (mac) in (\MAC(16-bit)): ", total_fwd_comp_mac/single_ann_mac)

        


if __name__ == '__main__':
    main()
