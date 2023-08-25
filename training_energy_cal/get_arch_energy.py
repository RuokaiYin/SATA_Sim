import argparse
import energy_configs
import mem_configs
import yaml


# def backward(energy_dic):


def get_arch_energy(args, mem_args, hw_config, fwd_b):
    
    arch_e_dic = {}

    with open(hw_config, 'r') as file:

        documents = yaml.full_load(file)
        energy_dic = (vars(args))

        single_lif = 0
        single_mac_fwd = 0
        single_pgu = 0
        single_mac_bwd = 0
        single_mac_wup = 0

        for item, doc in documents.items():
            if item == "fwd":
                for item2, doc2 in doc.items():
                    if item2 == "lif":
                        for k in doc2:
                            single_lif += (energy_dic[k] * (fwd_b/16)) * doc2[k]
                    elif item2 == "mac":
                        for k in doc2:
                            single_mac_fwd += (energy_dic[k] * (fwd_b/16)) * doc2[k]

            elif item == "bwd":
                for item2, doc2 in doc.items():
                    if item2 == "pgu":
                        for k in doc2:
                            single_pgu += energy_dic[k] * doc2[k]
                    elif item2 == "mac":
                        for k in doc2:
                            single_mac_bwd += energy_dic[k] * doc2[k]

            elif item == "wup":
                for item2, doc2 in doc.items():
                    if item2 == "mac":
                        for k in doc2:
                            single_mac_wup += energy_dic[k] * doc2[k]


    arch_e_dic['lif'] = single_lif
    arch_e_dic['mac_fwd'] = single_mac_fwd
    arch_e_dic['pgu'] = single_pgu
    arch_e_dic['mac_bwd'] = single_mac_bwd
    arch_e_dic['mac_wup'] = single_mac_wup

    arch_e_dic['dram_fwd']=mem_args.dram * (fwd_b/16)
    arch_e_dic['glb_fwd']=mem_args.sram * (fwd_b/16)
    arch_e_dic['spad_fwd']=mem_args.spad * (fwd_b/16)
    arch_e_dic['dram_bwd']=mem_args.dram
    arch_e_dic['glb_bwd']= mem_args.sram
    arch_e_dic['spad_bwd']=mem_args.spad
    arch_e_dic['dram_wup']=mem_args.dram
    arch_e_dic['glb_wup']=mem_args.sram
    arch_e_dic['spad_wup']=mem_args.spad


    return arch_e_dic
