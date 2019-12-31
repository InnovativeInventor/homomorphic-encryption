import random
import sys
import nufhe
import time

class Secrets:
    def __init__(self, a: int, b: int):
        ctx = nufhe.Context()
        self.secret_key, self.cloud_key = self.ctx.make_key_pair()
        if a and b
            self._a = self.convert_init(a)
            self._b = self.convert_init(b)
            self.encrypted_a = self.ctx.encrypt(self.secret_key, self._a)
            self.encrypted_b = self.ctx.encrypt(self.secret_key, self._b)
        else:
            self.random_init

    def random_init(self):
        self.bits1 = [False] + [random.choice([False, True]) for i in range(SIZE)]
        self.bits2 = [False] + [random.choice([False, True]) for i in range(SIZE)]
        self.ciphertext1 = ctx.encrypt(secret_key, self.bits1)
        self.ciphertext2 = ctx.encrypt(secret_key, self.bits2)
   

    def convert_init(self, a: int) -> list:
        """
        Don't forget to check that the list size is less than 31 
        """
        bin_a = bin(a)[2:]
        for each_chr in bin_a:

    def decrypt(self, a):
        return self.format_bitstr(self.ctx.decrypt(self.secret_key, a))

    def format_bitstr(self, bitstr):
        string = "".join([str(int(x)) for x in list(bitstr)])
        return int(string,2)

class Algebra:
    def __init__(self, ciphertext1, ciphertext2, cloud_key):
        """
        Can only play around with 31 bit data (final bit reserved for carry over)
        """
        self.size = 31
        vm = ctx.make_virtual_machine(cloud_key)

    def encrypted_adder(self, a, b, length):
        orig_a = a.copy()
        a = vm.gate_xor(a,b).copy()

        carryover = vm.gate_and(orig_a,b).copy()
        carryover.roll(-1)

        b = carryover
        if length == 0:
            return a
        return encrypted_adder(a, b, length - 1)

