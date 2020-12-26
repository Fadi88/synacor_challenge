import time


def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method ' + method.__name__ + ' took : ' +
              "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method


class vm:
    @profiler
    def __init__(self, _file):
        self.pc = 0
        self.stack = []
        self.txt = []
        self.terminated = False
        self.reg = [0] * 8
        with open(_file, 'rb') as f:
            b = f.read(2)
            while b != b'':
                self.txt.append(int.from_bytes(b, 'little', signed=False))
                b = f.read(2)

        self.ops_map = \
            {0: self.halt_0, 1: self.set_1, 2: self.push_2, 3: self.pop_3, 4: self.eq_4,
             5: self.gt_5, 6: self.jmp_6, 7: self.jt_7, 8: self.jf_8, 9: self.add_9,
             10: self.mul_10, 11: self.mod_11, 12: self.and_12, 13: self.or_13, 14: self.not_14,
             15: self.rmem_15, 16: self.wmem_16, 17: self.call_17,
             19: self.out_19, 21: self.noop_21}

    def get_value(self, offset):
        param = self.txt[self.pc + offset]
        if param < 32768:
            return param
        else:
            assert param <= 32775
            return self.reg[param - 32768]

    def set_value(self, offset, value):
        add = self.txt[self.pc + offset]
        if add < 32768:
            self.txt[add] = value
        else:
            self.reg[add - 32768] = value

    def set_address(self, add, value):
        if add < 32768:
            self.txt[add] = value
        else:
            self.reg[add - 32768] = value

    def halt_0(self):
        self.terminated = True

    def set_1(self):
        self.set_value(1, self.get_value(2))
        self.pc += 3

    def push_2(self):
        a = self.get_value(1)
        self.stack.append(a)
        self.pc += 2

    def pop_3(self):
        val = self.stack.pop()
        self.set_value(1, val)
        self.pc += 2

    def eq_4(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, b == c)
        self.pc += 4

    def gt_5(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, b > c)
        self.pc += 4

    def jmp_6(self):
        self.pc = self.get_value(1)

    def jt_7(self):
        if self.get_value(1) != 0:
            self.pc = self.get_value(2)
        else:
            self.pc += 3

    def jf_8(self):
        if self.get_value(1) == 0:
            self.pc = self.get_value(2)
        else:
            self.pc += 3

    def add_9(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, (b+c) % 32768)
        self.pc += 4

    def mul_10(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, (b*c) % 32768)
        self.pc += 4

    def mod_11(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, b % c)
        self.pc += 4

    def and_12(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, b & c)
        self.pc += 4

    def or_13(self):
        b = self.get_value(2)
        c = self.get_value(3)
        self.set_value(1, b | c)
        self.pc += 4

    def not_14(self):
        b = self.get_value(2)
        self.set_value(1, ~b & 0x7fff)
        self.pc += 3

    def rmem_15(self):
        add = self.txt[self.get_value(2)]
        self.set_value(1, add)
        self.pc += 3

    def wmem_16(self):
        val = self.get_value(2)
        self.set_address(self.txt[self.pc+1], val)
        # TOFIX: write at address of mem no in mem
        self.pc += 3

    def call_17(self):
        self.stack.append(self.pc + 2)
        self.pc = self.get_value(1)

    def out_19(self):
        print(chr(self.txt[self.pc + 1]), end='')
        self.pc += 2

    def noop_21(self):
        self.pc += 1

    def cycle(self):
        assert self.pc < len(self.txt)
        self.ops_map[self.txt[self.pc]]()

    @profiler
    def run(self):
        print()
        while not self.terminated:
            self.cycle()


if __name__ == "__main__":
    obj = vm('input/challenge.bin')
    obj.run()
