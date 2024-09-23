import argparse
import energy_configs
import yaml



def get_workload(T,b,network_path,sp_s):

    # network_path = 'vgg5_cifar10.yaml'
    workload_dic = {}

    with open(network_path,'r') as file:
        documents = yaml.full_load(file)

        #* Number of computation operations for the inference (currently supported in HAR paper)
        act_n = 0
        mac_fwd_n = 0

        #! Currently not supported (BWD, WUP stages and the memory operations)
        # pgu_n = 0
        # mac_bwd_n = 0
        # mac_wup_n = 0
        # dram_fwd_n =0 
        # glb_fwd_n =0 
        # spad_fwd_n =0 
        # dram_bwd_n =0 
        # glb_bwd_n =0  
        # spad_bwd_n =0 
        # dram_wup_n =0 
        # glb_wup_n =0 
        # spad_wup_n =0 

        

        for item, doc in documents.items():
            #! This mode is for the DCL network
            if doc['type'] == '2dconv':
                act_n += doc['out_s'] * doc['out_t'] * doc['w_cout'] * T
                mac_fwd_n += (1-sp_s) * (doc['w_kt'] * doc['w_ks']* doc['w_cin'] * doc['w_cout']) * doc['out_s'] * doc['out_t'] * T
                

            elif doc['type'] == '1dconv':
                act_n += doc['out'] * doc['w_cout'] * T
                mac_fwd_n += (1-sp_s) * (doc['w_k'] * doc['w_cin'] * doc['w_cout']) * doc['out'] * T
                print('mac_num: ', mac_fwd_n)
                print('act_num: ', act_n)

            elif doc['type'] == 'linear':
                act_n += 0 #! Since there's only one linear layer in the FCN as the output layer, we neglect the activation operations.
                mac_fwd_n += (1-sp_s) * doc['out'] * doc['in'] * T


    #* Number of computation operations for the inference (currently supported in HAR paper)
    workload_dic['act'] = act_n
    workload_dic['mac_fwd'] = mac_fwd_n

    return workload_dic


        