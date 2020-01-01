import random
import sys
import nufhe
import time

SIZE = 30
bits1 = [False] + [random.choice([False, True]) for i in range(SIZE)]
bits2 = [False] + [random.choice([False, True]) for i in range(SIZE)]

ctx = nufhe.Context()
secret_key, cloud_key = ctx.make_key_pair()

ciphertext1 = ctx.encrypt(secret_key, bits1)
ciphertext2 = ctx.encrypt(secret_key, bits2)

start_time = time.time()
vm = ctx.make_virtual_machine(cloud_key)

def encrypted_shifter(a):
    a.roll(-1)
    return a

def encrypted_adder(a, b, length):
    orig_a = a.copy()
    a = vm.gate_xor(a,b).copy()

    carryover = vm.gate_and(orig_a,b).copy()
    carryover.roll(-1)

    # shift_step = encrypted_shifter(carryover)
    # if shift_step == None:
        # return a

    b = carryover
    if length == 0:
        return a
    return encrypted_adder(a, b, length - 1)

def format_bitstr(bitstr):
    string = "".join([str(int(x)) for x in list(bitstr)])
    return int(string,2)


result = encrypted_adder(ciphertext1, ciphertext2, SIZE)

end_time = time.time()

result_bits = ctx.decrypt(secret_key, result)
assert format_bitstr(bits1) + format_bitstr(bits2) == format_bitstr(result_bits)
