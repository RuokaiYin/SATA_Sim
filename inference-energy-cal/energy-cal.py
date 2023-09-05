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
    
    cycle_stats = {}
    cycle_stats['total_cycles'] = 0.0
    cycle_stats['sram_i_reads'] = 0.0
    cycle_stats['sram_w_reads'] = 0.0
    cycle_stats['sram_o_writes'] = 0.0
    cycle_stats['dram_i_reads'] = 0.0
    cycle_stats['dram_w_reads'] = 0.0
    cycle_stats['dram_o_writes'] = 0.0

    if dataflow == 'sata':
        for layer, stats in data.items():
            # print((stats.get('SRAM OFMAP Start Cycle') + stats.get('SRAM OFMAP Cycles'))*timestep)
            cycle_stats['total_cycles'] += (stats.get('SRAM OFMAP Start Cycle') + stats.get('SRAM OFMAP Cycles'))*timestep
            cycle_stats['sram_i_reads'] += stats.get('SRAM IFMAP Reads')
            cycle_stats['sram_w_reads'] += stats.get('SRAM Filter Reads')
            cycle_stats['sram_o_writes'] += stats.get('SRAM OFMAP Writes')
            cycle_stats['dram_i_reads'] += stats.get('DRAM IFMAP Reads')
            cycle_stats['dram_w_reads'] += stats.get('DRAM Filter Reads')
            cycle_stats['dram_o_writes'] += stats.get('DRAM OFMAP Writes')
    else:
        for layer, stats in data.items():
            cycle_stats['total_cycles'] += stats.get('SRAM OFMAP Start Cycle') + stats.get('SRAM OFMAP Cycles')
            cycle_stats['sram_i_reads'] += stats.get('SRAM IFMAP Reads')
            cycle_stats['sram_w_reads'] += stats.get('SRAM Filter Reads')
            cycle_stats['sram_o_writes'] += stats.get('SRAM OFMAP Writes')
            cycle_stats['dram_i_reads'] += stats.get('DRAM IFMAP Reads')
            cycle_stats['dram_w_reads'] += stats.get('DRAM Filter Reads')
            cycle_stats['dram_o_writes'] += stats.get('DRAM OFMAP Writes')
    
    return cycle_stats
    


    # if dataflow == 'sata':
def comp_computation_energy(comp_filepath, cycle_dict, arch_configpath):
    
    with open(arch_configpath, 'r') as file:
        data = yaml.safe_load(file)
    subtrees_ = data.get('architecture', {}).get('subtree', [])
    for tree in subtrees_:
        if tree.get('class') == 'pe-array':
            attributes = tree.get('attributes')
            height = attributes.get('height')
            width  = attributes.get("width")
    pe_size = height * width
    arch = data.get('architecture')
    freq = arch.get('clock-frequency')
    cyc = 1/freq

    with open(mem_filepath, 'r') as file:
        comp_data = yaml.safe_load(file)
    comp_dic = {}
    



def comp_mem_energy(mem_filepath, cycle_dict, arch_configpath):

    with open(arch_configpath, 'r') as file:
        arch_data = yaml.safe_load(file)
    arch = arch_data.get('architecture')
    freq = arch.get('clock-frequency')
    cyc = 1/freq
    # timestep = arch.get('timestep')

    with open(mem_filepath, 'r') as file:
        data = yaml.safe_load(file)
    mem_dic = {}
    dram_entries = data.get('DRAM', [])
    total_dram = 0.0
    for entry in dram_entries:
        name = entry.get('name')
        sub_total = 0.0
        if name not in mem_dic:
            mem_dic[name] = {}
        mem_dic[name]['ifmap'] = entry.get('read energy') * cycle_dict['dram_i_reads'] # ? CHECK: is the energy in nJ ?
        total_dram += mem_dic[name]['ifmap']
        sub_total  += mem_dic[name]['ifmap']
        mem_dic[name]['weight'] = entry.get('read energy') * cycle_dict['dram_w_reads'] # ? CHECK: is the energy in nJ ?
        total_dram += mem_dic[name]['weight']
        sub_total  += mem_dic[name]['weight']
        mem_dic[name]['ofmap'] = entry.get('read energy') * cycle_dict['dram_o_writes'] # ? CHECK: is the energy in nJ ?
        total_dram += mem_dic[name]['ofmap']
        sub_total  += mem_dic[name]['ofmap']
        mem_dic[name]['total'] = sub_total
    mem_dic['dram_total'] = total_dram

    sram_entries = data.get('SRAM', [])
    total_sram = 0.0
    for entry in sram_entries:
        name = entry.get('name')
        if name not in mem_dic:
            mem_dic[name] = {}
        if 'ifmap' in name:
            mem_dic[name]['ifmap-dynamic'] = entry.get('read dynamic energy') * cycle_dict['sram_i_reads'] # ? CHECK: is the energy in nJ ?
            mem_dic[name]['ifmap-leakage'] = entry.get('leakage power') * cycle_dict['total_cycles'] * cyc
            mem_dic[name]['ifmap-total']= mem_dic[name]['ifmap-dynamic'] + mem_dic[name]['ifmap-leakage']
            total_sram += mem_dic[name]['ifmap-dynamic'] + mem_dic[name]['ifmap-leakage']
        elif 'weight' in name:
            mem_dic[name]['weight-dynamic'] = entry.get('read dynamic energy') * cycle_dict['sram_w_reads'] # ? CHECK: is the energy in nJ ?
            mem_dic[name]['weight-leakage'] = entry.get('leakage power') * cycle_dict['total_cycles'] * cyc
            mem_dic[name]['weight-total']= mem_dic[name]['weight-dynamic'] + mem_dic[name]['weight-leakage']
            total_sram += mem_dic[name]['weight-dynamic'] + mem_dic[name]['weight-leakage']
        elif 'ofmap' in name:
            mem_dic[name]['ofmap-dynamic'] = entry.get('write dynamic energy') * cycle_dict['sram_o_writes'] # ? CHECK: is the energy in nJ ?
            mem_dic[name]['ofmap-leakage'] = entry.get('leakage power') * cycle_dict['total_cycles'] * cyc
            mem_dic[name]['ofmap-total']= mem_dic[name]['ofmap-dynamic'] + mem_dic[name]['ofmap-leakage']
            total_sram += mem_dic[name]['ofmap-dynamic'] + mem_dic[name]['ofmap-leakage']
    mem_dic['sram_total'] = total_sram

    # print(mem_dic)
    file_path = './results/memory-energy.yaml'
    # print()
    with open(file_path, 'w') as yaml_file:
        yaml.dump(mem_dic, yaml_file, default_flow_style=False)
    return mem_dic


if __name__ == "__main__":
    cycle_path = './results/cycle-stat.yaml'
    arch_path = './sata-config.yaml'
    mem_path = './results/mem-stat.yaml'
    cycle_stat = read_cycles(cycle_path, arch_path)
    # print(cycle_stat)
    mem_dic = {}
    mem_dic = comp_mem_energy(mem_path, cycle_stat, arch_path)


