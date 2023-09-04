import yaml
import os

def read_cycles(cycle_filepath, arch_configpath):

    with open(arch_configpath, 'r') as file:
        data = yaml.safe_load(file)
    arch = data.get('architecture')
    dataflow = arch.get('dataflow')
    timestep = arch.get('timestep')

    with open(cycle_filepath, 'r') as file:
        data = yaml.safe_load(file)
    if dataflow == 'sata':

    else:
        total_cycles = data.get('SRAM OFMAP Start Cycle') + data.get('SRAM OFMAP Cycles')
        sram_i_reads = data.get('SRAM IFMAP Reads')
        sram_w_reads = data.get('')
        sram_o_writes = data.get('SRAM OFMAP Writes')
        dram_i_reads = data.get('DRAM IFMAP Reads')
        dram_w_reads = data.get('')
        dram_o_writes = ata.get('DRAM OFMAP Writes')
        
    
    # subtrees_ = data.get('architecture', {}).get('subtree', [])
    # for tree in subtrees_:
    #     if tree.get('class') == 'pe-array':
    #         attributes = tree.get('attributes')
    #         height = attributes.get('height')
    #         width  = attributes.get("width")
    # pe_size = height * width

    # if dataflow == 'sata':


def comp_l_energy(comp_filepath):

    with open(filename, 'r') as file:
        data = yaml.safe_load(file)



if __name__ == "__main__":

    energy_dic = {}


