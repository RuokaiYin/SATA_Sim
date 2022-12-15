import argparse
import energy_configs
import mem_configs
import yaml
from get_workload import get_workload
from get_arch_energy import get_arch_energy



def main():

    hw_config = 'sata_config.yaml'
    network_path = 'vgg5_cifar10.yaml'
    args = energy_configs.get_args()
    mem_args = mem_configs.get_args()
    single_ann_mac = 0.2779

    T = 8
    b = 8

    sp_s = 0.9
    sp_du = 0.7
    sp_df = 0.6

    total_energy = 0

    keyword = ['lif','mac_fwd','pgu','mac_bwd','mac_wup','dram_fwd', 'glb_fwd','spad_fwd','dram_bwd',
                'glb_bwd', 'spad_bwd', 'dram_wup', 'glb_wup', 'spad_wup']


    workload_d = get_workload(T,b,network_path,sp_s,sp_du,sp_df)
    arch_d = get_arch_energy(args, mem_args, hw_config)



    for k in keyword:
        total_energy += workload_d[k]*arch_d[k]


    print("Total Energy in (\MAC): ", total_energy/single_ann_mac)    

        


if __name__ == '__main__':
    main()
