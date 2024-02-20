from utils import oneD_linear_interpolation, oneD_quadratic_interpolation
import yaml

class Primitive_Computation_Unit:
    def __init__(self, name, bit_width, scaling = 'linear', info = {"area": 0,
                                                            "power-dynamic": 0,
                                                            "power-leakage": 0,
                                                            "access-latency": 0,
                                                            "cycle-time": 0}):
        self.name = name
        self.bit_width = bit_width
        self.info = info
        self.scaling = scaling
        self.access_counts = 0

    def set_bit_width(self, bit_width):
        self.bit_width = bit_width
    
    def set_name(self, name):
        self.name = name

    def set_info(self, info):
        self.info = info

    def get_area(self):
        return self.info["area"]
    
    #*                               *#
    #* This returns the power in pW. *#
    #*                               *#
    def get_dpower(self):
        return self.info["power-dynamic"]
    
    #*                               *#
    #* This returns the power in pW. *#
    #*                               *#
    def get_lpower(self):
        return self.info["power-leakage"]

    #*                                       *#
    #* The cycle time used in the synthesis. *# 
    #* Cycles taken from input to output.    *#
    #*                                       *#
    def get_cycletime(self):
        return self.info["cycle-time"]
    
    #*                                  *#
    #* This returns the data in cycles. *#
    #*                                  *#
    def get_access_latency(self):
        return self.info["access-latency"]

    #*                                                                                                     *#
    #* This function checks the provided synthesis file. If the stats already in the file, fill the stats. *#
    #* Otherwise, interpolate the bitwidth of the units to get the desired attributes.                     *#
    #*                                                                                                     *#
    def check_synthesis_file(self, key, synthesis_file_location):
        
        with open(synthesis_file_location, 'r') as file:
            data = yaml.safe_load(file)
        data = data.get(key,{})
        self.scaling = data['interpolation']
        for instance in data['already_syn']:
            if instance['bw'] == self.bit_width: #* The case where the provided bit_width is already existed in the synthesis file
                self.info['area'] = instance['attributes']['area']
                self.info['power-dynamic'] = instance['attributes']['power-dynamic']
                self.info['power-leakage'] = instance['attributes']['power-leakage']
                self.info['access-latency'] = instance['attributes']['access-latency']
                self.info['cycle-time'] = instance['attributes']['cycle-time']
            else: #* We scale the area and power with the interpolation.
                known_dict = data['already_syn']
                if self.scaling == 'linear':
                    self.info['area'] = oneD_linear_interpolation(self.bit_width, 'area', known_dict)
                    self.info['power-dynamic'] = oneD_linear_interpolation(self.bit_width, 'power-dynamic', known_dict)
                    self.info['power-leakage'] = oneD_linear_interpolation(self.bit_width, 'power-leakage', known_dict)
                else:
                    self.info['area'] = oneD_quadratic_interpolation(self.bit_width, 'area', known_dict)
                    self.info['power-dynamic'] = oneD_quadratic_interpolation(self.bit_width, 'power-dynamic', known_dict)
                    self.info['power-leakage'] = oneD_quadratic_interpolation(self.bit_width, 'power-leakage', known_dict)
                self.info['access-latency'] = instance['attributes']['access-latency']
                self.info['cycle-time'] = instance['attributes']['cycle-time']


    #*                                *#
    #* This returns the energy in pJ. *#
    #*                                *#
    def get_access_energy(self):
        return self.info["access-latency"] * self.info["cycle-time"] * self.info["power-dynamic"]
    

    #*                                     *#
    #* This returns the latency in cycles. *#
    #*                                     *#
    def get_latency(self):
        return self.info["access-latency"] * self.access_counts
    
    #*                                 *#
    #* This returns the # of accesses. *#
    #*                                 *#
    def get_accesses(self):
        return self.access_counts
    

    #*                                 *#
    #* This updates the # of accesses. *#
    #*                                 *#
    def update_accesses(self, accesses):
        self.access_counts += accesses



def test():
    mul = Primitive_Computation_Unit("mul_in_mac_spike", 16, 'linear')
    print(f'name of the instance: {mul.name}.')
    print(f'bitwidth of the instance: {mul.bit_width}.')

    print("Setting the bitwidth and name of the instance.")
    mul.set_name("new_mul")
    mul.set_bit_width(32)
    print(f'name of the instance: {mul.name}.')
    print(f'bitwidth of the instance: {mul.bit_width}.')

    info = {
            "area": 10,
            "power-dynamic": 5,
            "power-leakage": 3,
            "access-latency": 1,
            "cycle-time":1
        }
    mul.set_info(info)

    print("Area: ", mul.get_area())
    print("Dpower: ", mul.get_dpower())
    print("Lpower: ", mul.get_lpower())
    print("Latency: ", mul.get_latency())

def main():
    test()

if __name__ == "__main__":
    main()