import random
import sys
import nufhe
import time
import secrets

class Secrets:
    def __init__(self, a = None, b = None):
        self.size = 32
        self.ctx = nufhe.Context()
        self.secret_key, self.cloud_key = self.ctx.make_key_pair()
        if a and b:
            self.a = a
            self.b = b
            self.ciphertext_a = self.encrypt(self.a)
            self.ciphertext_b = self.encrypt(self.b)
        else:
            self.random_init()

    def random_init(self):
        self.a = secrets.randbits(31)
        self.b = secrets.randbits(31)

        self.ciphertext_a = self.encrypt(self.a)
        self.ciphertext_b = self.encrypt(self.b)

    def convert_init(self, a: int) -> list:
        """
        Don't forget to check that the list size is less than 31
        """
        bin_a = bin(a)[2:]
        bitlist = [False]*self.size
        for count, each_chr in enumerate(bin_a):
            bitlist[self.size - len(bin_a) + count] = bool(int(each_chr))

        return bitlist

    def decrypt(self, a):
        return self.format_bitstr(self.ctx.decrypt(self.secret_key, nufhe.LweSampleArray.loads(a, self.ctx.thread)))

    def encrypt(self, a):
        return self.ctx.encrypt(self.secret_key, self.convert_init(a)).dumps()

    def format_bitstr(self, bitlist):
        string = "".join([str(int(x)) for x in list(bitlist)])
        return int(string,2)

class Algebra:
    def __init__(self, ciphertext_a, ciphertext_b, cloud_key):
        """
        Can only play around with 31 bit data (final bit reserved for carry over)
        Assert ^
        """
        self.size = 32

        self.ctx = nufhe.Context()
        nufhe.clear_computation_cache(self.ctx.thread)
        self.vm = self.ctx.make_virtual_machine(cloud_key)
        self.ciphertext_a = nufhe.LweSampleArray.loads(ciphertext_a, self.ctx.thread)
        self.ciphertext_b = nufhe.LweSampleArray.loads(ciphertext_b, self.ctx.thread)
        # self.ciphertext_b = ciphertext_b

    def add(self):
        return self.encrypted_adder(self.ciphertext_a.copy(), self.ciphertext_b.copy(), self.size)

    def encrypted_adder(self, a, b, length):
        nufhe.clear_computation_cache(self.ctx.thread)
        print(length, type(a), type(b))
        orig_a = a.copy()
        a = self.vm.gate_xor(a, b).copy()

        carryover = self.vm.gate_and(orig_a, b).copy()
        carryover.roll(-1)

        b = carryover
        if length == 0:
            return a
        return self.encrypted_adder(a, b, length - 1)
