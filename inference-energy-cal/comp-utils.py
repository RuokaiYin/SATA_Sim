import yaml
import hw_kernels  # Assuming hw-kernels.py is in the same directory

# Function Definitions

def extract_act_dict_from_yaml(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    act_dict = {}

    def recursive_search(subtrees):
        for subtree in subtrees:
            if subtree.get('class') == 'pe-compute':
                locals_ = subtree.get('local', [])
                for local in locals_:
                    act_tag = local.get('act-tag')
                    attributes = local.get('attributes', {})
                    kernel_name = attributes.get('kernel')
                    count = attributes.get('count')
                    gated = attributes.get('gated')
                    width = attributes.get('width')

                    # Create the kernel object using the class from hw-kernels.py
                    KernelClass = getattr(hw_kernels, kernel_name, None)
                    if KernelClass:
                        kernel_obj = KernelClass(width)
                    else:
                        print(f"Warning: No matching class found for kernel: {kernel_name}")
                        kernel_obj = kernel_name  # Use the name as a fallback

                    if act_tag in act_dict:
                        act_dict[act_tag].append((kernel_obj, count, gated))
                    else:
                        act_dict[act_tag] = [(kernel_obj, count, gated)]
            elif subtree.get('class') == 'pe-mem':
                locals_ = subtree.get('local', [])
                for local in locals_:
                    act_tag = local.get('act-tag')
                    attributes = local.get('attributes', {})
                    kernel_name = attributes.get('kernel')
                    count = attributes.get('count')
                    gated = attributes.get('gated')
                    width = attributes.get('width')
                    size  = attributes.get('size-bytes')
                    
                     # Create the kernel object using the class from hw-kernels.py
                    KernelClass = getattr(hw_kernels, kernel_name, None)
                    if KernelClass:
                        kernel_obj = KernelClass(size)
                        # print(kernel_obj.get_dpower())
                    else:
                        print(f"Warning: No matching register-files found for kernel: {kernel_name}")
                        kernel_obj = kernel_name  # Use the name as a fallback
                    if act_tag in act_dict:
                        act_dict[act_tag].append((kernel_obj, count, gated))
                    else:
                        act_dict[act_tag] = [(kernel_obj, count, gated)]
                # print(act_dict)
            else:
                recursive_search(subtree.get('subtree', []))

    recursive_search(data.get('architecture', {}).get('subtree', []))
    return act_dict

def aggregate_act_data(act_dict):
    aggregated_data = {}

    for act_tag, kernel_list in act_dict.items():
        area_total = 0
        lpower_total = 0
        dpower = {'n': 0, 'y': 0}
        
        for kernel_obj, count, gated in kernel_list:
            # print(gated)
            area_total += kernel_obj.get_area() * count
            lpower_total += kernel_obj.get_lpower() * count
            dpower[gated] += kernel_obj.get_dpower() * count
            # if 'spad' in act_tag:
            

        # Restricting to 4 decimal places
        area_total = round(area_total, 6)
        lpower_total = round(lpower_total, 6)
        dpower['n'] = round(dpower['n'], 6)
        dpower['y'] = round(dpower['y'], 6)

        aggregated_data[act_tag] = {
            'area': area_total,
            'lpower': lpower_total,
            'dpower': dpower
        }

    return aggregated_data

# Main Execution

if __name__ == "__main__":
    filename = 'sata-config.yaml'
    act_dict = extract_act_dict_from_yaml(filename)
    # print(act_dict)
    aggregated_act_data = aggregate_act_data(act_dict)
    print(aggregated_act_data)

    output_filename = 'results/comp-stat.yaml'
    with open(output_filename, 'w') as outfile:
        yaml.dump(aggregated_act_data, outfile, default_flow_style=False)
    print(f"Computation components written to {output_filename}")