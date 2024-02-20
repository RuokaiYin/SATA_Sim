
class Primitive_Computation_Unit:
    def __init__(self, name, bit_width, 
                 scaling = 'linear', info = {"area": 0,
                                            "power-dynamic": 0,
                                            "power-leakage": 0,
                                            "access-latency": 0,
                                            "cycle-time": 0}):
        self.name = name
        self.bit_width = bit_width
        self.info = info
        self.scaling = scaling

    def set_bit_width(self, bit_width):
        self.bit_width = bit_width
    
    def set_name(self, name):
        self.name = name

    def set_info(self, info):
        self.info = info

    def get_area(self):
        return self.info["area"]
    
    def get_dpower(self):
        return self.info["power-dynamic"]
    
    def get_lpower(self):
        return self.info["power-leakage"]

    #* The cycle time used in the synthesis. Cycles taken from input to output. *#
    def get_cycletime(self):
        return self.info["cycle-time"]
    
    #*                                  *#
    #* This returns the data in cycles. *#
    #*                                  *#
    def get_latency(self):
        return self.info["access-latency"]
    
    def get_access_energy(self):
        return self.info["access-latency"] * self.info["cycle-time"] * self.info["power-dynamic"]
    
    #! TODO: to implement this based on interpolation.
    def scale_info(self, new_bw):
        return 0



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