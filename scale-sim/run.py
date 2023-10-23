import subprocess
import argparse
import csv
import yaml
import re
import shutil
import os

def run_command(command):
    """Execute the given command and return True if successful, False otherwise."""
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"Error executing the command: {' '.join(command)}")
        return False
    return True

def extract_data(filepath, dataflow):
    # Create a dictionary to store the extracted information with the desired hierarchy
    extracted_data = {}
    extracted_data_os = {}
    extracted_data_ws = {}

    for path in filepath:
        # Open the CSV file
        if dataflow == "sata":
            
            if path[-29:-27] == "os":
                with open(path, 'r') as file:
                    reader = csv.DictReader(file)
                    # Loop through each row in the CSV
                    for row in reader:
                        # Strip spaces from keys
                        row = {k.strip(): v for k, v in row.items()}
                        
                        layer_data = {
                            "SRAM IFMAP Reads": float(row["SRAM IFMAP Reads"]),
                            "SRAM OFMAP Writes": float(row["SRAM OFMAP Writes"]),
                            "DRAM IFMAP Reads": float(row["DRAM IFMAP Reads"]),
                            "DRAM OFMAP Writes": float(row["DRAM OFMAP Writes"]),
                            "SRAM IFMAP Cycles": (float(row["SRAM IFMAP Stop Cycle"])-float(row["SRAM IFMAP Start Cycle"])),
                            "SRAM OFMAP Cycles": (float(row["SRAM OFMAP Stop Cycle"])-float(row["SRAM OFMAP Start Cycle"])),
                            "SRAM OFMAP Start Cycle": float(row["SRAM OFMAP Start Cycle"])
                        }
                        # Use LayerID as the key for the outer dictionary
                        extracted_data_os["Layer " + row["LayerID"]] = layer_data

            elif path[-29:-27] == "ws":
                with open(path, 'r') as file:
                    reader = csv.DictReader(file)
                    # Loop through each row in the CSV
                    for row in reader:
                        # Strip spaces from keys
                        row = {k.strip(): v for k, v in row.items()}
                        
                        layer_data = {
                             "SRAM Filter Reads": float(row["SRAM Filter Reads"]),
                             "DRAM Filter Reads": float(row["DRAM Filter Reads"]),
                             "SRAM Filter Cycles": (float(row["SRAM Filter Stop Cycle"])-float(row["SRAM Filter Start Cycle"]))
                        }
                        # Use LayerID as the key for the outer dictionary
                        extracted_data_ws["Layer " + row["LayerID"]] = layer_data
            else:
                print("Error! Unsupported dataflow in SATA's dataflow.")
                exit()
            
        else:
            with open(path, 'r') as file:
                reader = csv.DictReader(file)
                # Loop through each row in the CSV
                for row in reader:
                    # Strip spaces from keys
                    row = {k.strip(): v for k, v in row.items()}
                    
                    layer_data = {
                        "SRAM IFMAP Reads": float(row["SRAM IFMAP Reads"]),
                        "SRAM Filter Reads": float(row["SRAM Filter Reads"]),
                        "SRAM OFMAP Writes": float(row["SRAM OFMAP Writes"]),
                        "DRAM IFMAP Reads": float(row["DRAM IFMAP Reads"]),
                        "DRAM Filter Reads": float(row["DRAM Filter Reads"]),
                        "DRAM OFMAP Writes": float(row["DRAM OFMAP Writes"]),
                        "SRAM IFMAP Cycles": (float(row["SRAM IFMAP Stop Cycle"])-float(row["SRAM IFMAP Start Cycle"])),
                        "SRAM OFMAP Cycles": (float(row["SRAM OFMAP Stop Cycle"])-float(row["SRAM OFMAP Start Cycle"]))
                    }
                    
                    # Use LayerID as the key for the outer dictionary
                    extracted_data["Layer " + row["LayerID"]] = layer_data

    # Define the output path for the YAML file
    output_path = '../inference-energy-cal/results/cycle-stat.yaml'
    if dataflow == 'sata':
        # extracted_data.update(extracted_data_ws)
        # print(extracted_data)
        # extracted_data.update(extracted_data_os)
        # print(extracted_data)
        merged_dict = {}

        for layer, subdict1 in extracted_data_ws.items():
            if layer in extracted_data_os:
                subdict2 = extracted_data_os[layer]
                merged_dict[layer] = {**subdict1, **subdict2}
            else:
                merged_dict[layer] = subdict1

        for layer, subdict2 in extracted_data_os.items():
            if layer not in extracted_data_ws:
                merged_dict[layer] = subdict2
        # print(merged_dict)
    # Write the extracted data to a YAML file
    with open(output_path, 'w') as yaml_file:
        yaml.dump(merged_dict, yaml_file, default_flow_style=False)
    
    print("Succefully written the extracted cycle stats!")


if __name__ == "__main__":

    default_config_path = "./configs/running.cfg"
    with open(default_config_path, 'r') as config_file:
        content = config_file.read()

    # Search for the pattern "Dataflow : value" in the content
    match = re.search(r"Dataflow\s*:\s*([^\n]+)", content)
    
    if match:
        dataflow =  match.group(1).strip()  # Return the matched value
    else:
        print("Dataflow not found in the config file.")
    # print(dataflow)
    
    if dataflow == "os" or dataflow =="ws":
        command = ['python3', 'scalesim/scale.py', '-t', 'topologies/sata/VGG9-test.csv', '-c', default_config_path, '-p', './running_results']
        success = run_command(command)
        if not success:
            print("Running scalesim for os/ws dataflow is failed.")
    elif dataflow == 'sata':
        # print("test")
    # elif dataflow == "sata":

        output_config_path = ["./configs/running_ws.cfg","./configs/running_os.cfg"]
        report_list = []
        for file in output_config_path:
            shutil.copy(default_config_path, file)
            with open(file, 'r') as f:
                original_content = f.read()
            # print(file[-6:-4])
            updated_content = re.sub(r"(Dataflow\s*:\s*)[^\n]+", r"\1" + file[-6:-4], original_content)

            # Apply the second replacement to the already updated content
            updated_content = re.sub(r"(run_name\s*=\s*)([^\n]+)", r"\1\2-" + file[-6:-4], updated_content)
            # print(updated_content)

            # Write the combined updated content back to the config file
            with open(file, 'w') as config_file:
                config_file.write(updated_content)
                # Apply the first replacement



            command = ['python3', 'scalesim/scale.py', '-t', 'temp_workload.csv', '-c', file, '-p', './running_results']
            success = run_command(command)
            if not success:
                print("Running scalesim for sata dataflow is failed: " + file[-6:-4])
                exit()
            else:
                with open(file, 'r') as f:
                    content = f.read()
                name = re.search(r"run_name\s*=\s*([^\n]+)", content)
                report_list.append('./running_results/'+ name.group(1).strip() + '/DETAILED_ACCESS_REPORT.csv')
    # dataflow = 'sata'
    # report_list = ['./running_results/SATA-inference-os/DETAILED_ACCESS_REPORT.csv', './running_results/SATA-inference-ws/DETAILED_ACCESS_REPORT.csv']
    extract_data(report_list,dataflow)
    folder_to_clean = './running_results/'
    for filename in os.listdir(folder_to_clean):
        file_path = os.path.join(folder_to_clean, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    if len(output_config_path)!= 0:
        for temp in output_config_path:
            os.remove(temp)
    os.remove('temp_workload.csv')
    os.remove('./configs/running.cfg')
    print("Cycle stats generated done. Done with cleanning the temp stat files.")