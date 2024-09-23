import argparse
import energy_configs
import yaml


class Workload_Calculator:
    """The Calculator to Get Total Workload"""

    def __init__(self, mapping='TF', network_path=None, sp_dic=None, T=8):
        

        self.timstep = T
        self.sp_du = sp_dic['du']
        self.sp_s = sp_dic['s']
        self.sp_df = sp_dic['df']

        L = 0
        with open(network_path,'r') as file:
            documents = yaml.full_load(file)
            for item, doc in documents.items():
                L += 1
        self.layer = L
    
    def cal(self):

        print(self.layer)
        
        return None

def get_workload(T,b,network_path,sp_s,sp_du,sp_df):

    # network_path = 'vgg5_cifar10.yaml'
    workload_dic = {}

    with open(network_path,'r') as file:
        documents = yaml.full_load(file)
        
        T = 8
        b = 8
        lif_n = 0
        mac_fwd_n = 0
        pgu_n = 0
        mac_bwd_n = 0
        mac_wup_n = 0
        dram_fwd_n =0 
        glb_fwd_n =0 
        spad_fwd_n =0 
        dram_bwd_n =0 
        glb_bwd_n =0  
        spad_bwd_n =0 
        dram_wup_n =0 
        glb_wup_n =0 
        spad_wup_n =0 

        

        for item, doc in documents.items():
            if doc['type'] == '2dconv':
                lif_n += doc['K'] * doc['E_h'] * doc['E_w'] * T
                mac_fwd_n += (1-sp_s) * doc['C']* doc['R_h'] * doc['R_w'] * doc['K'] * doc['E_h'] * doc['E_w']  * T
                pgu_n += doc['K'] * doc['E_h'] * doc['E_w'] * T
                mac_bwd_n += (1-sp_du) * doc['C']* doc['R_h'] * doc['R_w'] * doc['K'] * doc['H_h'] * doc['H_w']  * T
                mac_wup_n += (1-sp_s) * doc['C']* doc['R_h'] * doc['R_w'] * doc['K'] * doc['E_h'] * doc['E_w']  * T

                dram_fwd_n += doc['K'] * doc['C']* doc['R_h'] * doc['R_w'] + (doc['K'] * doc['E_h'] * doc['E_w'] + (1/b) * doc['C'] * doc['H_h'] * doc['H_w']) * T
                glb_fwd_n += 2 * (doc['K'] * doc['C']* doc['R_h'] * doc['R_w'] + (doc['K'] * doc['E_h'] * doc['E_w'] + (1/b) * doc['C'] * doc['H_h'] * doc['H_w']) * T)
                spad_fwd_n += 2 * (doc['K'] * doc['C']* doc['R_h'] * doc['R_w'] + T * (1/b) * doc['C'] * doc['H_h'] * doc['H_w'])
                dram_bwd_n += T * (doc['K'] * doc['E_h'] * doc['E_w'] + (1/b) * doc['C'] * doc['H_h'] * doc['H_w'])
                glb_bwd_n += 7 * T * (doc['K'] * doc['E_h'] * doc['E_w']) + (2*T*(1/b)*doc['C'] * doc['H_h'] * doc['H_w'] + doc['K'] * doc['C']* doc['R_h'] * doc['R_w'])
                spad_bwd_n += doc['K'] * doc['C']* doc['R_h'] * doc['R_w'] + T * doc['K'] * doc['E_h'] * doc['E_w']
                dram_wup_n += 2 * (doc['K'] * doc['C']* doc['R_h'] * doc['R_w'])
                glb_wup_n += 2* (1+T) * doc['K'] * doc['C']* doc['R_h'] * doc['R_w'] + T * ((1/b) * doc['C'] * doc['H_h'] * doc['H_w']+doc['K'] * doc['E_h'] * doc['E_w'])
                spad_wup_n += 2* (1+T) * doc['K'] * doc['C']* doc['R_h'] * doc['R_w'] + T * ((1/b) * doc['C'] * doc['H_h'] * doc['H_w']+doc['K'] * doc['E_h'] * doc['E_w']) + 2*T*doc['K'] * doc['C']* doc['R_h'] * doc['R_w']

            elif doc['type'] == 'linear':
                lif_n += doc['out'] * T
                mac_fwd_n = doc['out'] * doc['in'] * T
                pgu_n += doc['out'] * T
                mac_bwd_n += doc['out'] * doc['in'] * T
                mac_wup_n += doc['out'] * doc['in'] * T

                dram_fwd_n += doc['out'] * doc['in'] + doc['out']*T + doc['in']*T*(1/b)
                glb_fwd_n += 2*(doc['out'] * doc['in'] + doc['out']*T + doc['in']*T*(1/b))
                spad_fwd_n += 2*(doc['out'] * doc['in'] + T * (1/b) * doc['in'])
                dram_bwd_n += T*(doc['out'] + (1/b)*doc['in'])
                glb_bwd_n +=  7*T*(doc['out']) + (2*T*(1/b)*doc['in'] + doc['in']*doc['out'])
                spad_bwd_n += (doc['out'] * doc['in'] + T*doc['out'])
                dram_wup_n += 2 * doc['out'] * doc['in']
                glb_wup_n += 2 * (1+T) * doc['out'] * doc['in'] + T * ((1/b) * doc['in'] + doc['out'])
                spad_wup_n += 2 * (1+T) * doc['out'] * doc['in'] + T * ((1/b) * doc['in'] + doc['out']) + 2*T*doc['out'] * doc['in']


    workload_dic['lif'] = lif_n
    workload_dic['mac_fwd']=mac_fwd_n
    workload_dic['pgu']=pgu_n
    workload_dic['mac_bwd']=mac_bwd_n
    workload_dic['mac_wup']=mac_wup_n
    workload_dic['dram_fwd']=dram_fwd_n
    workload_dic['glb_fwd']=glb_fwd_n
    workload_dic['spad_fwd']=spad_fwd_n
    workload_dic['dram_bwd']=dram_bwd_n
    workload_dic['glb_bwd']= glb_bwd_n
    workload_dic['spad_bwd']=spad_bwd_n
    workload_dic['dram_wup']=dram_wup_n
    workload_dic['glb_wup']=glb_wup_n
    workload_dic['spad_wup']=spad_wup_n


    return workload_dic


        