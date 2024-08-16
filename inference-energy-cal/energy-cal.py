import yaml
import os
import math

def read_cycles(cycle_filepath, arch_configpath, workload_filepath):

    with open(arch_configpath, 'r') as file:
        data = yaml.safe_load(file)
    arch = data.get('architecture')
    dataflow = arch.get('dataflow')
    with open(workload_filepath, 'r') as file:
        work_data = yaml.safe_load(file)
    general = work_data.get('General')
    timestep = general.get('timestep')

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
            cycle_stats['total_cycles'] += (stats.get('SRAM OFMAP Start Cycle') + stats.get('SRAM OFMAP Cycles')) * timestep + stats.get('SRAM Filter Cycles')
            cycle_stats['sram_i_reads'] += stats.get('SRAM IFMAP Reads')
            cycle_stats['sram_w_reads'] += stats.get('SRAM Filter Reads')
            # cycle_stats['sram_o_writes'] += stats.get('SRAM OFMAP Writes') #! This is the arxived version where the writing of psum is not considered.
            cycle_stats['sram_o_writes'] += stats.get('SRAM OFMAP Writes') * timestep
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
    

def extract_workload(workload_filepath):
    
    with open(workload_filepath, 'r') as file:
        work_data = yaml.safe_load(file)
    general = work_data.get('General')
    timestep = general.get('timestep')
    sparsity = general.get('sparsity')

    workload_dic = {}
    layers = work_data.get('Layers', {})
    total_mac = 0.0
    total_lif = 0.0

    for l in layers:
        attr = l['attributes']
        name = l['name']
        if 'Conv' in name:
            of_w = (math.floor((attr['IFMAP Width'] + 2 - attr['Filter Width'])/attr['Strides']) + 1) # TODO: Adding support for different padding, now assume 1
            of_h = (math.floor((attr['IFMAP Height'] + 2 - attr['Filter Height'])/attr['Strides']) + 1)
            total_lif += attr['Num Filter'] * (of_w * of_h) * timestep
            total_mac += attr['Num Filter'] * (of_w * of_h) * (attr['Filter Width'] * attr['Filter Height'] * attr['Channels']) * timestep * (1-sparsity)
        elif 'FC' in name: #! Added support for FC.
            total_mac += attr['Num Filter'] * attr['Channels'] * timestep * (1-sparsity)
            total_lif += attr['Num Filter'] * timestep
    
    workload_dic['total_mac'] = int(total_mac)
    workload_dic['total_lif'] = int(total_lif)
    
    return workload_dic


def comp_computation_energy(comp_filepath, cycle_dict, arch_configpath, workload_dict):
    
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
    freq = arch.get('clock-frequency') * 1000000 #! Need to convert to MHz first, in yaml, M is not take into consideration
    cyc = 1/freq

    with open(comp_filepath, 'r') as file:
        comp_data = yaml.safe_load(file)

    comp_dic = {}
    total_comp = 0.0
    for component, values in comp_data.items():
        comp_dic[component] = {}
        subtotal = 0.0
        if 'lif' in component:
            workload = workload_dict['total_lif']
        else:
            workload = workload_dict['total_mac']
        # ! Power of computation unit is in mW, from the comp-stat.yaml
        convert_ratio = 1000000 # ! Need to convert it back to nJ, to align with the memory energy, which is in nJ
        for key, value in values.items():
            if isinstance(value, dict):
                comp_dic[component]['energy-operation'] = value['y'] * workload * cyc * convert_ratio 
                subtotal += comp_dic[component]['energy-operation']
                comp_dic[component]['energy-ungated'] = value['n']*cycle_dict['total_cycles'] * cyc * convert_ratio * pe_size
                subtotal += comp_dic[component]['energy-ungated']
            elif 'lpower' in key:
                comp_dic[component]['energy-leakage'] = value * cycle_dict['total_cycles'] * cyc * convert_ratio * pe_size
                subtotal += comp_dic[component]['energy-leakage']
        comp_dic[component]['total'] = subtotal
        total_comp += subtotal
    comp_dic['total'] = total_comp

    comp_dic['total_mac_ops'] = workload_dic['total_mac']
    comp_dic['total_activation_ops'] = workload_dic['total_lif']

    file_path = './results/computation-energy.yaml'
    # print()
    with open(file_path, 'w') as yaml_file:
        yaml.dump(comp_dic, yaml_file, default_flow_style=False)
    return comp_dic


def comp_mem_energy(mem_filepath, cycle_dict, arch_configpath):

    with open(arch_configpath, 'r') as file:
        arch_data = yaml.safe_load(file)
    arch = arch_data.get('architecture')
    freq = arch.get('clock-frequency') * 1000000 #! Need to convert to MHz first, in yaml, M is not take into consideration
    cyc = 1/freq
    x_bw = arch.get('act-prec')
    w_bw = arch.get('weight-prec')
    o_bw = arch.get('output-prec')
    convert_ratio = 1000000 #! Need again to convert SRAM leakage to nJ, the leaking power is in mW from the mem-stats.yaml

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
        mem_dic[name]['ifmap'] = entry.get('read energy') * (x_bw/8) * cycle_dict['dram_i_reads'] # ? CHECK: is the energy in nJ ?
        total_dram += mem_dic[name]['ifmap']
        sub_total  += mem_dic[name]['ifmap']
        mem_dic[name]['weight'] = entry.get('read energy') * (w_bw/8) * cycle_dict['dram_w_reads'] # ? CHECK: is the energy in nJ ?
        total_dram += mem_dic[name]['weight']
        sub_total  += mem_dic[name]['weight']
        mem_dic[name]['ofmap'] = entry.get('read energy') * (o_bw/8) * cycle_dict['dram_o_writes'] # ? CHECK: is the energy in nJ ?
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
            mem_dic[name]['ifmap-dynamic'] = entry.get('read dynamic energy') * (x_bw/8) * cycle_dict['sram_i_reads'] # ? CHECK: is the energy in nJ ?
            mem_dic[name]['ifmap-leakage'] = entry.get('leakage power') * cycle_dict['total_cycles'] * cyc * convert_ratio #! The power is in mW, need to scale it to nJ
            mem_dic[name]['ifmap-total']= mem_dic[name]['ifmap-dynamic'] + mem_dic[name]['ifmap-leakage']
            total_sram += mem_dic[name]['ifmap-dynamic'] + mem_dic[name]['ifmap-leakage']
        elif 'weight' in name:
            mem_dic[name]['weight-dynamic'] = entry.get('read dynamic energy') * (w_bw/8) * cycle_dict['sram_w_reads'] # ? CHECK: is the energy in nJ ?
            mem_dic[name]['weight-leakage'] = entry.get('leakage power') * cycle_dict['total_cycles'] * cyc * convert_ratio
            mem_dic[name]['weight-total']= mem_dic[name]['weight-dynamic'] + mem_dic[name]['weight-leakage']
            total_sram += mem_dic[name]['weight-dynamic'] + mem_dic[name]['weight-leakage']
        elif 'ofmap' in name:
            mem_dic[name]['ofmap-dynamic'] = entry.get('write dynamic energy') * (o_bw/8) * cycle_dict['sram_o_writes'] # ? CHECK: is the energy in nJ ?
            mem_dic[name]['ofmap-leakage'] = entry.get('leakage power') * cycle_dict['total_cycles'] * cyc * convert_ratio
            mem_dic[name]['ofmap-total']= mem_dic[name]['ofmap-dynamic'] + mem_dic[name]['ofmap-leakage']
            total_sram += mem_dic[name]['ofmap-dynamic'] + mem_dic[name]['ofmap-leakage']
    
    mem_dic['sram_total'] = total_sram
    mem_dic['total'] = total_dram + total_sram

    file_path = './results/memory-energy.yaml'
    with open(file_path, 'w') as yaml_file:
        yaml.dump(mem_dic, yaml_file, default_flow_style=False)
    return mem_dic


if __name__ == "__main__":

    cycle_path = './results/cycle-stat.yaml'
    arch_path = './arch-config.yaml'
    mem_path = './results/mem-stat.yaml'
    comp_path = './results/comp-stat.yaml'
    # work_path = './workloads/workload_direct.yaml'
    work_path = './workload.yaml'

    cycle_stat = read_cycles(cycle_path, arch_path, work_path)
    workload_dic = extract_workload(work_path)
    mem_dic = comp_mem_energy(mem_path, cycle_stat, arch_path)
    comp_dic = comp_computation_energy(comp_path, cycle_stat, arch_path, workload_dic)
    
    print("SATA_Sim simulaton successes. Please go to the result folder to locate the energy results.")

