from compute_instance import Primitive_Computation_Unit


synthesis_file_location = './arith_32nm-2_5ns.yaml'

class Multiplier(Primitive_Computation_Unit):
    def __init__(self, name, bit_width):
        super().__init__(name, bit_width)
        self.name = name
        self.bit_width = bit_width
        self.check_synthesis_file('MUL',synthesis_file_location)


class Accumulator(Primitive_Computation_Unit):
    def __init__(self, name, bit_width):
        super().__init__(name, bit_width)
        self.name = name
        self.bit_width = bit_width
        self.check_synthesis_file('ACC',synthesis_file_location)

class Adder(Primitive_Computation_Unit):
    def __init__(self, name, bit_width):
        super().__init__(name, bit_width)
        self.name = name
        self.bit_width = bit_width
        self.check_synthesis_file('ADD',synthesis_file_location)


class Register(Primitive_Computation_Unit):
    def __init__(self, name, bit_width):
        super().__init__(name, bit_width)
        self.name = name
        self.bit_width = bit_width
        self.check_synthesis_file('REG',synthesis_file_location)


def test():
    mul = Multiplier('m1', 16)
    print(mul.get_area())
    mul = Multiplier('m2', 8)
    print(mul.get_area())


def main():
    test()

if __name__ == "__main__":
    main()