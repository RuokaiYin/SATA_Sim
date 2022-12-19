# SATA_Sim

## Overview

SATA_Sim is an energy estimation framework for Backpropagation-Through-Time (BPTT) based Spiking Neural Networks (SNNs) training with sparsity awareness.

## Prerequisite

Python (Version >= 3.6)

## Citing
If you find SATA_Sim is useful for your research, please use the following bibtex to cite us,

```
@article{yin2022sata,
  title={SATA: Sparsity-Aware Training Accelerator for Spiking Neural Networks},
  author={Yin, Ruokai and Moitra, Abhishek and Bhattacharjee, Abhiroop and Kim, Youngeun and Panda, Priyadarshini},
  journal={arXiv preprint arXiv:2204.05422},
  year={2022}
}
```

## Simple Usage Example
<p>Please first provide the shape information of the network by writing a yaml file like the vgg5_cifar10.yaml. <br>
Then please specific the architecture like sata_config.yaml. You can directly use the sata_config.yaml to use the architecture of SATA.<br>
Then please specific the dynamic energy of the computation components in energy_configs.py. You can directly use the energy_configs.py for SATA.<br>
Then please specific the dynamic energy of the computation components in energy_configs.py. You can directly use the energy_configs.py for SATA.<br>
Please also specific the dynamic energy of memory components in mem_configs.py. This information can be got by using CACTI.<br>
Then please specific the timesteps, all three kinds of sparsity, bitwidth of parameters other than spikes in energy_cal.py.<br>
Finally, run the energy_cal.py, you will get the energy estimation that normalized with the energy of a single MAC operation in ANNs.</p>

## Contribution
Active contributor:
1. [Ruokai Yin](https://ruokaiyin.github.io/)

Please contact me (ruokai.yin@yale.edu) if you are interested in contributing to this project!

## TODO:
The current code is a preliminary version. The current codes can support the estimation of forward computation energy.

The estimation of backward and weight update computation will be added. :white_check_mark:

The estimation of memory acess energy of forward, backward, and weight update stages will be added. :white_check_mark:

The instructions of using the codes will be added. :white_check_mark:

Supporting the configurable bitwidth for internal datapaths.

Supporting the other dataflow mappings other than the one used in SATA.

Supporting the estimation mode that considers the leak energy.
