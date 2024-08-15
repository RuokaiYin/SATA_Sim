import subprocess
import csv
import yaml

# Run the external command
command = ['python3', 'scalesim/scale.py', '-t', 'topologies/sata/VGG9.csv', '-c', 'configs/scale.cfg', '-p', './results/SATA/']
result = subprocess.run(command, capture_output=True, text=True, shell=True)

# Check if the command executed successfully
if result.returncode != 0:
    print("Error executing the command:")
    print(result.stderr)
    exit(1)

# Define the file path
file_path = './results/SATA/SATA_128_original/DETAILED_ACCESS_REPORT.csv'

# Create a dictionary to store the extracted information with the desired hierarchy
extracted_data = {}

# Open the CSV file
with open(file_path, 'r') as file:
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
output_path = './results/SATA/SATA_128_original/extracted_data.yaml'

# Write the extracted data to a YAML file
with open(output_path, 'w') as yaml_file:
    yaml.dump(extracted_data, yaml_file, default_flow_style=False)
