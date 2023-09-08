import hw_kernels
import importlib

adder = hw_kernels.adder(8)
mul = hw_kernels.multiplier(8)
reg = hw_kernels.register(8)
mac_8_bit = adder.get_dpower() + mul.get_dpower() + reg.get_dpower()
acc_8_bit = adder.get_dpower() + reg.get_dpower()
scale = 1/250

#########################   TDBN   ###################################

# The work provide the estimate adds and muls numbers

add_n = 1.8e9
mul_n = 3.4e7

# Assuming 8 bits, 300MHz
adder = hw_kernels.adder(8)
mul = hw_kernels.multiplier(8)

tdbn_total_estimated_energy = (add_n*adder.get_dpower() + mul_n*mul.get_dpower()) * scale

print('TDBN estimated energy in (/8-bit int MAC): ', round(tdbn_total_estimated_energy,2))


#########################   TSSL   ###################################

Conv = [128, 256,'m',512,'m',1024,'m',512]
Linear = [1024,512]
T = 5
spa = 0.901

kernel_size = 3*3
input_channel = 3
img_size = 32

n_acc = 0
for c in Conv:
    if type(c) is int:
        n_acc += input_channel*kernel_size*c*img_size*img_size
        input_channel = c
    else:
        img_size = img_size/2
n_acc =  n_acc + (512*img_size*img_size*1024) + 1024*512
tssl_total_estimated_energy = (n_acc * acc_8_bit * T * (1-spa)) * scale

print('TSSL estimated energy in (/8-bit int MAC): ', round(tssl_total_estimated_energy,2))


#########################   Direct   #################################

Conv = [128,256,'m',512,'m',1024,'m',512]
Linear = [1024,512]
T = 10
spa = 0.90

kernel_size = 3*3
input_channel = 3
img_size = 32

n_acc = 0
for c in Conv:
    if type(c) is int:
        n_acc += input_channel*kernel_size*c*img_size*img_size
        input_channel = c
    else:
        img_size = img_size/2
n_acc =  n_acc + (512*img_size*img_size*1024) + 1024*512
tssl_total_estimated_energy = (n_acc * acc_8_bit * T * (1-spa)) * scale
print('Direct estimated energy in (/8-bit int MAC): ', round(tssl_total_estimated_energy,2))



#########################   BNTT   #################################

Conv = [64, 64, "M", 128, 128, "M", 256, 256, 256, "M"]
Linear = [1024,512]
T = 20
spa = 0.91

kernel_size = 3*3
input_channel = 3
img_size = 32

W_size = 0
U_size = 0
w_bit = 8
u_bit = 32
membrane_size = img_size
batch = 1

n_acc = 0
for c in Conv:
    if type(c) is int:
        n_acc += input_channel*kernel_size*c*img_size*img_size
        U_size += c*(membrane_size**2)*batch
        W_size += input_channel*c*kernel_size
        input_channel = c
    else:
        img_size = img_size/2
        membrane_size = membrane_size/2
n_acc =  n_acc + (512*img_size*img_size*1024) + 1024*512
# print(n_acc)
tssl_total_estimated_energy = (n_acc * acc_8_bit * T * (1-spa)) * scale
print('BNTT estimated energy in (/8-bit int MAC): ', round(tssl_total_estimated_energy,2))


#########################   SBP   #################################

Conv = [64, 64, "M", 128, 128, "M", 256, 256, 256, "M"]
Linear = [1024,512]
T = 50
spa = 0.9

kernel_size = 3*3
input_channel = 3
img_size = 32

W_size = 0
U_size = 0
w_bit = 8
u_bit = 32
membrane_size = img_size
batch = 1

n_acc = 0
for c in Conv:
    if type(c) is int:
        n_acc += input_channel*kernel_size*c*img_size*img_size
        U_size += c*(membrane_size**2)*batch
        W_size += input_channel*c*kernel_size
        input_channel = c
    else:
        img_size = img_size/2
        membrane_size = membrane_size/2
n_acc =  n_acc + (512*img_size*img_size*1024) + 1024*512
# print(n_acc)
sbp_total_estimated_energy = (n_acc * acc_8_bit * T * (1-spa)) * scale
print('SBP estimated energy in (/8-bit int MAC): ', round(sbp_total_estimated_energy,2))



#########################   LTH   #################################
energy_cal = importlib.import_module("energy-cal")

dic = energy_cal.extract_workload('./workloads/workload_lth.yaml')
n_acc = dic['total_mac']
lth_total_estimated_energy = n_acc * acc_8_bit * scale
print('LTH estimated energy in (/8-bit int MAC): ', round(lth_total_estimated_energy,2))


# U_size = U_size + 1024 + 512
# U_size = U_size*u_bit/8 ### bits to MB

# W_size += (512*img_size*img_size*1024) + 1024*512

# W_size = W_size*w_bit/8 ### bits to MB

# print('U size', U_size)
# print('W size', W_size)

# print(acc_8_bit*1e-3*(1/300e6))