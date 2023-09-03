import numpy as np
import torch
import torch.nn as nn

class register(nn.Module):
    def __init__(self, width=16):
        super(register, self).__init__()
        self.q = 0.
        self.d = 0.
        self.width = width

        ### bw : um^2
        self.area_dic = {
            2:  9.24,
            4:  17.47,
            8:  34.27,
            16: 68.04,
            32: 135.07
        }
        ### mw
        self.d_power = {
            2:  (5.81e-04 + 2.61e-03),
            4:  (1.17e-03 + 5.20e-03),
            8:  (2.19e-03 + 1.03e-02),
            16: (4.41e-03 + 2.07e-02),
            32: (8.55e-03 + 4.12e-02)
        }
        ### uw
        self.l_power = {
            2:  (5.42e-03),
            4:  (1.02e-02),
            8:  (2.01e-02),
            16: (4.02e-02),
            32: (8.02e-02)
        }

    def forward(self, x):
        self.q = self.d
        self.d = x

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class registerfiles(nn.Module):
    def __init__(self, size=16):
        super(registerfiles , self).__init__()
        self.q = 0.
        self.d = 0.
        self.size = size ## Size in bytes

        self.byte = register(width = 8)
        self.byte_area = self.byte.get_area()
        self.byte_dpower = self.byte.get_dpower()
        self.byte_lpower = self.byte.get_lpower()

    def forward(self, x):
        self.q = self.d
        self.d = x

    def get_area(self):
        ### Return unit in mm^2
        return self.size*self.byte_area
    
    def get_dpower(self):
        ### Return unit in mw
        return self.size*self.byte_dpower

    def get_lpower(self):
        ### Return unit in mw
        return self.size*self.byte_lpower
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class comparator(nn.Module):
    def __init__(self, width=16):
        super(comparator, self).__init__()
        self.width = width
        ### bw : um^2
        self.area_dic = {
            2:  (2.856),
            4:  (7.056),
            8:  (15.456),
            16: (32.424),
            32: (66.360)
        }
        ### mw
        self.d_power = {
            2:  (8.71e-04 + 4.52e-04),
            4:  (2.64e-03 + 1.00e-03),
            8:  (6.70e-03 + 2.38e-03),
            16: (1.46e-02 + 4.95e-03),
            32: (3.18e-02 + 1.07e-02)
        }
        ### uw
        self.l_power = {
            2:  (1.56e-03),
            4:  (3.98e-03),
            8:  (8.76e-03),
            16: (1.82e-02),
            32: (3.71e-02)
        }

    def forward(self, in0, in1):
        out = float(in0 < in1)
        return out

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class lfsr_rng(nn.Module):
    def __init__(self, width=32):
        super(lfsr_rng, self).__init__()
        assert width == 32, "Current lfsr RNG only supports 32-bits"
        self.width = width
        ### bw : um^2
        self.area_dic = {
            2:  (),
            4:  (),
            8:  (),
            16: (),
            32: (89.88)
        }
        ### mw
        self.d_power = {
            2:  (),
            4:  (),
            8:  (),
            16: (),
            32: (3.52e-02)
        }
        ### uw
        self.l_power = {
            2:  (),
            4:  (),
            8:  (),
            16: (),
            32: (5.12e-02)
        }

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class fifo(nn.Module):
    def __init__(self, width=32, depth=8):
        super(fifo, self).__init__()
        self.width = width
        self.depth = depth

        ################## Depth 2 ##################
        self.area_dic_2 = {
            1:  (11.0880),
            2:  (18.6480),
            4:  (35.4480),
            8:  (69.2160),
            16: (134.9040),
            32: (269.9760)
        }
        self.d_power_2 = {
            1:  (6.39e-04 + 2.47e-03),
            2:  (9.39e-04 + 4.97e-03),
            4:  (1.68e-03 + 9.87e-03),
            8:  (3.26e-03 + 1.96e-02),
            16: (6.04e-03 + 3.90e-02),
            32: (1.26e-02 + 7.83e-02)
        }
        self.l_power_2 = {
            1:  (6.63e-03),
            2:  (1.05e-02),
            4:  (2.04e-02),
            8:  (3.97e-02),
            16: (7.76e-02),
            32: (0.156)
        }
        ################## Depth 4 ##################
        self.area_dic_4 = {
            1:  (17.9760),
            2:  (35.1120),
            4:  (68.3760),
            8:  (137.9280),
            16: (273.000),
            32: (540.1200)
        }
        self.d_power_4 = {
            1:  (8.39e-04 + 4.87e-03),
            2:  (1.39e-03 + 9.65e-03),
            4:  (2.78e-03 + 1.91e-02),
            8:  (5.90e-03 + 3.84e-02),
            16: (1.15e-02 + 7.69e-02),
            32: (2.22e-02 + 0.153)
        }
        self.l_power_4 = {
            1:  (1.26e-02),
            2:  (1.99e-02),
            4:  (3.89e-02),
            8:  (7.93e-02),
            16: (0.157),
            32: (0.310)
        }
        ################## Depth 8 ##################
        self.area_dic_8 = {
            1:  (35.1120),
            2:  (68.3760),
            4:  (137.9280),
            8:  (271.3200),
            16: (540.1200),
            32: (1079.4000)
        }
        self.d_power_8 = {
            1:  (1.20e-03 + 9.40e-03),
            2:  (2.43e-03 + 1.87e-02),
            4:  (5.42e-03 + 3.78e-02),
            8:  (9.68e-03 + 7.49e-02),
            16: (1.99e-02 + 0.150),
            32: (3.93e-02 + 0.300)
        }
        self.l_power_8 = {
            1:  (1.98e-02),
            2:  (3.87e-02),
            4:  (7.88e-02),
            8:  (0.155),
            16: (0.309),
            32: (0.616)
        }
        assert depth < 16, "Current FIFO-depth only supports below 16"
        ## Depth prior
        self.area_dic = {
            2: self.area_dic_2,
            4: self.area_dic_4,
            8: self.area_dic_8
        }
        self.d_power = {
            2: self.d_power_2,
            4: self.d_power_4,
            8: self.d_power_8
        }
        self.l_power = {
            2: self.l_power_2,
            4: self.l_power_4,
            8: self.l_power_8
        }

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.depth][self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.depth][self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.depth][self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class multiplier(nn.Module):
    def __init__(self, width=16):
        super(multiplier, self).__init__()
        self.width = width
        ### bw : um^2
        self.area_dic = {
            2:  (3.528),
            4:  (23.016),
            8:  (101.472),
            16: (441.504),
            32: (1797.264)
        }
        ### mw
        self.d_power = {
            2:  (1.00e-03 + 5.51e-04),
            4:  (7.60e-03 + 4.58e-03),
            8:  (4.82e-02 + 3.39e-02),
            16: (0.307    + 0.204),
            32: (1.664    + 1.122)
        }
        ### uw
        self.l_power = {
            2:  (1.96e-03),
            4:  (1.29e-02),
            8:  (6.13e-02),
            16: (0.279),
            32: (1.166)
        }

    def forward(self, in0, in1):
        out = in0 * in1
        return out

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class adder(nn.Module):
    def __init__(self, width=16):
        super(adder, self).__init__()
        self.width = width
        ### bw : um^2
        self.area_dic = {
            2:  (4.704),
            4:  (13.776),
            8:  (22.176),
            16: (45.024),
            32: (90.72)
        }
        ### mw
        self.d_power = {
            2:  (1.02e-03 + 1.45e-03),
            4:  (4.44e-03 + 4.29e-03),
            8:  (7.62e-03 + 9.27e-03),
            16: (1.68e-02 + 1.99e-02),
            32: (3.49e-02 + 4.09e-02)
        }
        ### uw
        self.l_power = {
            2:  (3.07e-03),
            4:  (8.60e-03),
            8:  (1.70e-02),
            16: (3.50e-02),
            32: (7.08e-02)
        }

    def forward(self, in0, in1):
        out = in0 + in1
        return out

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

##############################################################

class subtractor(nn.Module):
    def __init__(self, width=16):
        super(subtractor, self).__init__()
        self.width = width
        ### bw : um^2
        self.area_dic = {
            2:  (4.704),
            4:  (13.776),
            8:  (22.176),
            16: (45.024),
            32: (90.72)
        }
        ### mw
        self.d_power = {
            2:  (1.02e-03 + 1.45e-03),
            4:  (4.44e-03 + 4.29e-03),
            8:  (7.62e-03 + 9.27e-03),
            16: (1.68e-02 + 1.99e-02),
            32: (3.49e-02 + 4.09e-02)
        }
        ### uw
        self.l_power = {
            2:  (3.07e-03),
            4:  (8.60e-03),
            8:  (1.70e-02),
            16: (3.50e-02),
            32: (7.08e-02)
        }

    def forward(self, in0, in1):
        out = in0 + in1
        return out

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total

###############################################################

class andgate(nn.Module):
    def __init__(self, width=16):
        super(andgate, self).__init__()
        self.width = width
        ### bw : um^2
        self.area_dic = {
            2:  (1.680),
            4:  (3.360),
            8:  (6.720),
            16: (13.44),
            32: (26.88)
        }
        ### mw
        self.d_power = {
            2:  (3.42e-04 + 2.55e-04),
            4:  (6.77e-04 + 5.04e-04),
            8:  (1.35e-03 + 1.00e-03),
            16: (2.72e-03 + 2.02e-03),
            32: (5.44e-03 + 4.05e-03)
        }
        ### uw
        self.l_power = {
            2:  (1.20e-03),
            4:  (2.41e-03),
            8:  (4.81e-03),
            16: (9.62e-03),
            32: (1.92e-02)
        }

    def forward(self, in0, in1):
        out = float(in0 & in1)
        return out

    def get_area(self):
        ### Return unit in mm^2
        return self.area_dic[self.width]/1000000.
    
    def get_dpower(self):
        ### Return unit in mw
        return self.d_power[self.width]

    def get_lpower(self):
        ### Return unit in mw
        return self.l_power[self.width]/1000.
    
    def get_total_power(self):
        total = self.get_dpower()+self.get_lpower
        ### Return unit in mw
        return total