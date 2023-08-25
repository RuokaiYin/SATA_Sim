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

    T = 4
    fwd_b = 2

    sp_s = 0.9
    sp_du = 0.7
    sp_df = 0.6


    keyword = ['lif','mac_fwd','pgu','mac_bwd','mac_wup','dram_fwd', 'glb_fwd','spad_fwd','dram_bwd',
                'glb_bwd', 'spad_bwd', 'dram_wup', 'glb_wup', 'spad_wup']


    workload_d = get_workload(T,fwd_b,network_path,sp_s,sp_du,sp_df)
    arch_d = get_arch_energy(args, mem_args, hw_config, fwd_b)


    total_energy = 0
    total_fwd_comp = 0
    total_fwd_mem = 0

    for k in keyword:
        total_energy += workload_d[k]*arch_d[k]

        if 'lif' in k:
            total_fwd_comp += workload_d[k]*arch_d[k]
        if 'mac_fwd' in k:
            total_fwd_comp += workload_d[k]*arch_d[k]
        elif 'fwd' in k:
            total_fwd_mem += workload_d[k]*arch_d[k]


    single_ann_mac = 0.239 + 0.0389
    print("Bitwidth for fwd: ", fwd_b)
    print("Total Energy in (\MAC): ", total_energy/single_ann_mac)
    print("Total Fwd Energy in (\MAC): ", (total_fwd_comp + total_fwd_mem)/single_ann_mac)
    print("Total Fwd Comp Energy in (\MAC): ", total_fwd_comp/single_ann_mac)  
    print("Total Fwd Mem  Energy in (\MAC): ", total_fwd_mem/single_ann_mac)

        


if __name__ == '__main__':
    main()
