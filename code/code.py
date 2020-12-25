import time

def profiler(method):
    def wrapper_method(*arg, **kw):
        t = time.time()
        ret = method(*arg, **kw)
        print('Method '  + method.__name__ +' took : ' + "{:2.5f}".format(time.time()-t) + ' sec')
        return ret
    return wrapper_method

class vm:
    @profiler
    def __init__ (self,_file):
        self.pc = 0
        self.reg = [0] * 8
        self.stack = []
        self.txt = []
        self.terminated = False
        with open(_file, 'rb') as f:
            b = f.read(2)
            while b != b'' :
                self.txt.append(int.from_bytes(b , 'little',False))
                b = f.read(2)
    def get_value(self,add):
        if add < 32768 :
            return add
        else :
            return self.reg[add - 32768]

    def set_value(self,add,val):
        if add < 32768 :
            self.txt[add] = val
        else :
            self.reg[add-32768] = val

    def cycle(self):

        assert self.pc < len(self.txt)
    
        inst = self.txt[self.pc]
        if inst == 0:
            self.terminated = True
        elif inst == 1:
            self.reg[32768-self.txt[self.pc+1]] = self.txt[self.pc + 2]
            self.pc += 3
        elif inst == 2:
            a = self.get_value(self.txt[self.pc+1])
            self.stack.append(a)
            self.pc += 2
        elif inst == 3:
            self.set_value(self.txt[self.pc+1],self.stack.pop())
            self.pc += 2
        elif inst == 4:
            b = self.get_value(self.txt[self.pc+2])
            c = self.get_value(self.txt[self.pc+3])
            self.set_value(self.txt[self.pc+1],b==c)
            self.pc += 4
        elif inst == 5:
            b = self.get_value(self.txt[self.pc+2])
            c = self.get_value(self.txt[self.pc+3])
            self.set_value(self.txt[self.pc+1],b>c)
            self.pc += 4
        elif inst == 6:
            a = self.txt[self.pc + 1]
            if a < 32768:
                self.pc = a
            else :
                self.reg[a - 32768] = a
        elif inst == 7:
            a = self.get_value(self.txt[self.pc + 1])
            b = self.get_value(self.txt[self.pc + 2])
            if a != 0:
                self.pc = b
            else :
                self.pc += 3
        elif inst == 8:
            a = self.get_value(self.txt[self.pc+1])
            b = self.get_value(self.txt[self.pc+2])
            if a == 0:
                self.pc = b
            else :
                self.pc += 3
        elif inst == 9:
            b = self.get_value(self.txt[self.pc+2])
            c = self.get_value(self.txt[self.pc+3])
            self.set_value(self.txt[self.pc+1],b+c)
            self.pc += 4
        elif inst == 12:
            b = self.get_value(self.txt[self.pc+2])
            c = self.get_value(self.txt[self.pc+3])
            self.set_value(self.txt[self.pc+1],b&c)
            self.pc += 4
        elif inst == 13:
            b = self.get_value(self.txt[self.pc+2])
            c = self.get_value(self.txt[self.pc+3])
            self.set_value(self.txt[self.pc+1],b|c)
            self.pc += 4
        elif inst == 19:
            print(chr(self.txt[self.pc +1]), end='')
            self.pc += 2
        elif inst == 21:
            self.pc += 1
        else :
            raise Exception('unsupported instruction ' , inst)

    @profiler
    def run(self):
        print()
        while not self.terminated:
            self.cycle()

if __name__ == "__main__":
    obj = vm('../input/challenge.bin')
    obj.run()
