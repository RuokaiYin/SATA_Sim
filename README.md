# SATA_Sim

## What's New:
**2024-Sep-23:**

We recently uploaded the HAR simulation codes for reproducing the computation energy results in the paper:

 <Li, Y., Yin, R., Kim, Y., & Panda, P. (2023). Efficient human activity recognition with spatio-temporal spiking neural networks. Frontiers in Neuroscience, 17, 1233037.>

 The codes can be found under the folder of /har_simulation.


**2024-Feb-20:**

A new and more rigorous version of SATA_Sim will be released soon...

**2023-Sep-6:**

A new version of SATA_Sim that supports cycle-accurate energy simulation for SNN inference is online! A more detailed READMe file will be added soon.

The new version of SATA_Sim takes into consideration both dynamic energy and leakage energy while counting all the data movement energy. 

The new version of SATA_Sim even lets you modify the hardware architecture if required.

We use cacti-7.0 and scale-sim-v2 as the backbone to simulate the memory component and to get the cycle statics.

For a quick start:

1. Clone the project, download all the dependencies, and go to the inference-energy-cal folder.
2. Modify the workload.yaml for your targeting workload, and modify the sata-config.yaml if any hardware architecture level changes are needed.
3. Simply run 'python3 run.py' and find the computation and memory energy results in the results folder. Some of the other related statistics are also provided in the folder.
4. The simulation might be running slow for large workloads.

Please do leave a message if any new features are needed. Happy running simulations on SNNs! Go Spike!


**2023-Mar-15:**

SATA_Sim now supports the different operand sizes (weights and membrane potentials) for the forward-stage energy estimation.

One useful case is to use the tool to estimate the energy cost improvement of the quantized SNN models (both weight and membrane potential quantization is supported).

To check the energy cost for different operand sizes, simply change the 'fwd_b' variable in the energy_cal.py to the target operand size. Please note that we assume the weights and membrane potentials are always quantized to the same bit-width.



## Overview

SATA_Sim is an energy estimation framework for Backpropagation-Through-Time (BPTT) based Spiking Neural Networks (SNNs) training with sparsity awareness.

## Prerequisite

Python (Version >= 3.6)

## Citing
If you find SATA_Sim is useful for your research, please use the following bibtex to cite us,

```
@article{yin2022sata,
  title={Sata: Sparsity-aware training accelerator for spiking neural networks},
  author={Yin, Ruokai and Moitra, Abhishek and Bhattacharjee, Abhiroop and Kim, Youngeun and Panda, Priyadarshini},
  journal={IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems},
  year={2022},
  publisher={IEEE}
}
```

## Simple Usage Example
<p>Please first provide the shape information of the network by writing a yaml file like the vgg5_cifar10.yaml. <br>
Then please specify the architecture like sata_config.yaml. You can directly use the sata_config.yaml to use the architecture of SATA.<br>
Then please specify the dynamic energy of the computation components in energy_configs.py. You can directly use the energy_configs.py for SATA.<br>
Then please specify the dynamic energy of the computation components in energy_configs.py. You can directly use the energy_configs.py for SATA.<br>
Please also specify the dynamic energy of memory components in mem_configs.py. This information can be obtained by using CACTI.<br>
Then please specify the timesteps, all three kinds of sparsity, bitwidth of parameters other than spikes in energy_cal.py.<br>
Finally, run the energy_cal.py, and you will get the energy estimation that is normalized with the energy of a single MAC operation in ANNs.</p>

## Contribution
Active contributor:
1. [Ruokai Yin](https://ruokaiyin.github.io/)

Please contact me (ruokai.yin@yale.edu) if you are interested in contributing to this project!

## TODO:

A more detailed READMe file will be added for using the new version of SATA_Sim.

The estimation of backward and weight update computation will be added. :white_check_mark:

The estimation of memory access energy of forward, backward, and weight update stages will be added. :white_check_mark:

The instructions for using the codes will be added. :white_check_mark:

Supporting the configurable bitwidth for internal fwd datapaths. :white_check_mark:

Supporting the configurable bitwidth for internal bwd & wup datapaths.

Supporting the other dataflow mappings other than the one used in SATA. :white_check_mark:

Supporting the estimation mode that considers the leak energy. :white_check_mark:
