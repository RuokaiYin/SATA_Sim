import argparse
import energy_configs
import mem_configs
import yaml


def get_arch_energy(energy_args, mem_args, hw_config, fwd_b):
    
    arch_e_dic = {}

    with open(hw_config, 'r') as file:

        documents = yaml.full_load(file)
        energy_dic = energy_args

        single_act = 0
        single_mac_fwd = 0

        #! Currently not supported (BWD, WUP stages and the memory operations)
        # single_pgu = 0
        # single_mac_bwd = 0
        # single_mac_wup = 0

        for item, doc in documents.items(): #! This goes through the yaml items in the watch_config.yaml
            if item == "fwd":
                for item2, doc2 in doc.items():
                    if item2 == "act":
                        for k in doc2:
                            #? the fwd_b is the precision of the weight operands. 
                            #? Here we divide by 16 since the energy value in the energy_config.yaml is for 16-bit precision.
                            single_act += (energy_dic[k] * (fwd_b/16)) * doc2[k]
                    elif item2 == "mac":
                        for k in doc2:
                            single_mac_fwd += (energy_dic[k] * (fwd_b/16)) * doc2[k]

            elif item == "bwd":
                #! TODO: to be implemented
                continue

            elif item == "wup":
                #! TODO: to be implemented
                continue


    arch_e_dic['act'] = single_act
    arch_e_dic['mac_fwd'] = single_mac_fwd

    print('single_act: ', single_act)
    print('single_mac_fwd: ', single_mac_fwd)

    return arch_e_dic
