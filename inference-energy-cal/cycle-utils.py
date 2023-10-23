import yaml
import os
import shutil
import subprocess
import csv

# Function Definitions

def extract_scalesim_dict_from_yaml(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

    scalesim_dict = {}

    def recursive_search(subtrees):
        for subtree in subtrees:
            if subtree.get('class') == 'glbs':
                locals_ = subtree.get('local', [])
                # print(locals_)
                for local in locals_:
                    act_tag = local.get('act-tag')
                    attributes = local.get('attributes', {})
                    size = int(attributes.get('size-bytes')/1024)

                    #! Adding support for multiple srams for one operand (e.g., 2 sram for ifmap)
                    if "weight" in act_tag:
                        scalesim_dict["FilterSramSzkB"] = size
                    elif "ifmap" in act_tag:
                        scalesim_dict["IfmapSramSzkB"] = size
                    elif "ofmap" in act_tag:
                        scalesim_dict["OfmapSramSzkB"] = size
                    else:
                        print(f"Warning: No matching sram class found for scalesim: {act_tag}")
            elif subtree.get('class') == 'pe-array':
                attributes = subtree.get('attributes', {})
                scalesim_dict["ArrayWidth"] = attributes.get("width")
                scalesim_dict["ArrayHeight"] = attributes.get("height")
            else:
                recursive_search(subtree.get('subtree', []))

    recursive_search(data.get('architecture', {}).get('subtree', []))
    if not "OfmapSramSzkB" in scalesim_dict.keys():
        scalesim_dict["OfmapSramSzkB"] = scalesim_dict["IfmapSramSzkB"]

    arch = data.get('architecture')
    dataflow = arch.get('dataflow')
    name = arch.get('name')
    scalesim_dict['run_name'] = name
    scalesim_dict['dataflow'] = dataflow

    return scalesim_dict

def update_config(yaml_filename, default_config_path, output_config_path):
    # Load the YAML file
    with open(yaml_filename, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # Define a mapping from the placeholders to the YAML keys
    mapping = {
        "x0": "run_name",
        "x1": "ArrayHeight",
        "x2": "ArrayWidth",
        "x3": "IfmapSramSzkB",
        "x4": "FilterSramSzkB",
        "x5": "OfmapSramSzkB",
        "x6": "dataflow"
    }

    # Copy the original default.cfg to a new file
    shutil.copy(default_config_path, output_config_path)

    # Load the copied file
    with open(output_config_path, 'r') as config_file:
        config_content = config_file.read()

    # Replace the placeholders with the values from the YAML file
    for placeholder, key in mapping.items():
        value = yaml_data.get(key, placeholder)  # Use the placeholder as default if key not found

        config_content = config_content.replace(placeholder, str(value))

    # Write the updated content back to the copied file
    with open(output_config_path, 'w') as config_file:
        config_file.write(config_content)

    print(f"{output_config_path} updated successfully!")


def generate_temp_workload():
    with open('./workload.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # Convert YAML data to CSV rows
    csv_rows = []
    for layer in data.get('Layers', []):
        attributes = layer.get('attributes', {})
        row = [
            layer.get('name', 'N/A'),
            attributes.get('IFMAP Height', 'N/A'),
            attributes.get('IFMAP Width', 'N/A'),
            attributes.get('Filter Height', 'N/A'),
            attributes.get('Filter Width', 'N/A'),
            attributes.get('Channels', 'N/A'),
            attributes.get('Num Filter', 'N/A'),
            attributes.get('Strides', 'N/A'),
            ''
        ]
        csv_rows.append(row)

    # Write the CSV data to a file
    csv_file_path = '../scale-sim/temp_workload.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Layer name', 'IFMAP Height', 'IFMAP Width', 'Filter Height', 'Filter Width', 'Channels', 'Num Filter', 'Strides', ''])
        csv_writer.writerows(csv_rows)

    print("CSV file written successfully.")

# Main Execution

if __name__ == "__main__":
    filename = 'sata-config.yaml'
    scalesim_dict = extract_scalesim_dict_from_yaml(filename)
    # print(scalesim_dict)
    scalesim_path = '../scale-sim'

    output_filename = 'cycle-stat-temp.yaml'
    with open(output_filename, 'w') as outfile:
        yaml.dump(scalesim_dict, outfile, default_flow_style=False)
    print(f"Cycle stats written to {output_filename}")


    default_config_path = os.path.join('..', 'scale-sim', 'configs', 'default.cfg')
    output_config_path = os.path.join('..', 'scale-sim', 'configs', 'running.cfg')

    # Update the copied file with values from the YAML file
    update_config(output_filename, default_config_path, output_config_path)
    os.remove(output_filename)
    generate_temp_workload()
    os.chdir(scalesim_path)
    subprocess.run('python3 run.py', shell=True)
