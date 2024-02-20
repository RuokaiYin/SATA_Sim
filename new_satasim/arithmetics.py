from compute_instance import Primitive_Computation_Unit
from utils import oneD_linear_interpolation, oneD_quadratic_interpolation
import yaml

synthesis_file_location = './arith_32nm-2_5ns.yaml'



def check_synthesis_file(unit, key):

    global synthesis_file_location
    
    with open(synthesis_file_location, 'r') as file:
        data = yaml.safe_load(file)
    data = data.get(key,{})
    unit.scaling = data['interpolation']
    for instance in data['already_syn']:
        if instance['bw'] == unit.bit_width: #* The case where the provided bit_width is already existed in the synthesis file
            unit.info['area'] = instance['attributes']['area']
            unit.info['power-dynamic'] = instance['attributes']['power-dynamic']
            unit.info['power-leakage'] = instance['attributes']['power-leakage']
            unit.info['access-latency'] = instance['attributes']['access-latency']
            unit.info['cycle-time'] = instance['attributes']['cycle-time']
        else: #* We scale the area and power with the interpolation.
            known_dict = data['already_syn']
            if unit.scaling == 'linear':
                unit.info['area'] = oneD_linear_interpolation(unit.bit_width, 'area', known_dict)
                unit.info['power-dynamic'] = oneD_linear_interpolation(unit.bit_width, 'power-dynamic', known_dict)
                unit.info['power-leakage'] = oneD_linear_interpolation(unit.bit_width, 'power-leakage', known_dict)
            else:
                unit.info['area'] = oneD_quadratic_interpolation(unit.bit_width, 'area', known_dict)
                unit.info['power-dynamic'] = oneD_quadratic_interpolation(unit.bit_width, 'power-dynamic', known_dict)
                unit.info['power-leakage'] = oneD_quadratic_interpolation(unit.bit_width, 'power-leakage', known_dict)
            unit.info['access-latency'] = instance['attributes']['access-latency']
            unit.info['cycle-time'] = instance['attributes']['cycle-time']


class Multiplier(Primitive_Computation_Unit):
    def __init__(self, name, bit_width):
        super().__init__(name, bit_width)
        self.name = name
        self.bit_width = bit_width
        check_synthesis_file(self,'MUL')


def test():
    mul = Multiplier('m1', 16)
    print(mul.get_area())
    mul = Multiplier('m2', 8)
    print(mul.get_area())


def main():
    test()

if __name__ == "__main__":
    main()