import argparse
import energy_configs
import yaml



def main():
    args = energy_configs.get_args()
    density = 0.5189

    hw_config = 'sata_ann_watch_config.yaml'
    network_config = 'dcl_shar.yaml'

    with open(hw_config, 'r') as file:

        documents = yaml.full_load(file)
        energy_dic = (vars(args))

        single_lif = 0
        single_mac = 0
        single_relu = 0

        for item, doc in documents.items():
            if item == "lif":
                for k in doc:
                    single_lif += energy_dic[k] * doc[k]
            elif item == "relu":
                for k in doc:
                    single_relu += energy_dic[k] * doc[k]
            elif item == "mac":
                for k in doc:
                    single_mac += energy_dic[k] * doc[k]

    with open(network_config,'r') as file:
        documents = yaml.full_load(file)
        
        act_n = 0
        mac_n = 0

        for item, doc in documents.items():
            if item[0] == 'c':
                mac_n += doc['w_k'] * doc['w_cin'] * doc['w_cout'] * doc['out']
                act_n += doc['w_cout'] * doc['out']
            elif item[0] == 'f':
                mac_n += doc['in'] * doc['out']
            elif item[0:3] == '2dc':
                mac_n += doc['w_kt'] * doc['w_ks'] * doc['w_cin'] * doc['w_cout'] * doc['out_s'] *doc['out_t']
                act_n += doc['out_s'] * doc['out_t'] * doc['w_cout']

    single_ann_mac = 0.2779

    if 'ann' in hw_config:
        total_comp_energy = (single_relu*act_n + single_mac*mac_n*density)/single_ann_mac
    else:
        total_comp_energy = (single_lif*act_n + single_mac*mac_n*density)/single_ann_mac

    
    print("Total Computation Energy in (\MAC): ", total_comp_energy)    
        # print(single_lif)
        # print(single_mac)
        


if __name__ == '__main__':
    main()