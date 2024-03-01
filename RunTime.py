import pandas as pd
from tabulate import tabulate

class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1
    
    def push(self,x):
        self.stack.append(x)
        self.top += 1

    def pop(self):
        if self.top == -1:
            print("Underflow error")
            return -1
        self.top -= 1
        return self.stack.pop()
    
class Function:
    def __init__(self, name):
        self.name = name
        self.d = {"int":0,"char":0,"bool":0,"float":0,"doub":0}

    def update(self,i,j,buffer):
        keys = set(self.d.keys())
        if ')' not in buffer[i]:
            start = i
            while ')' not in buffer[start]:
                if 'int' in buffer[start]:
                    self.d['int'] += 1
                elif 'float' in buffer[start]:
                    self.d['float'] += 1
                elif 'double' in buffer[start]:
                    self.d['double'] += 1
                elif 'char' in buffer[start]:
                    self.d['char'] += 1
                elif 'bool' in buffer[start]:
                    self.d['bool'] += 1
                start += 1
        for candidate in range(i,j+1):
            c = buffer[candidate]
            if c in keys:
                self.d[c] += 1
            elif c == 'double':
                self.d['doub'] += 1
            elif '[' in c:
                a = ""
                for i in c:
                    if i.isdigit():
                        a = a + i
                self.d[buffer[candidate-1]] += (int(a) + 1)
            elif c == 'struct':
                if buffer[candidate + 1] not in keys:
                    self.d[buffer[candidate+1]] = 1
                else:
                    self.d[buffer[candidate+1]] += 1
            else:
                pass
    
    def allocateMem(self):
        for dtype in self.d:
            self.d[dtype] = self.d[dtype] * size[dtype]

    def display(self):
        total_mem = 0
        temp_dict ={"S.No": [], "Object Type" : [], "Number Of Objects" : [], "Size Allocated" : []}
        print("FUNCTION: ",self.name)
        i = 0
        for dtype in self.d:
            if self.d[dtype] != 0:
                i += 1
                temp_dict["S.No"].append(i)
                temp_dict["Object Type"].append(dtype)
                temp_dict["Number Of Objects"].append(self.d[dtype]//size[dtype])
                temp_dict["Size Allocated"].append(self.d[dtype])
                total_mem += self.d[dtype]

        df = pd.DataFrame.from_dict(temp_dict)
        print("------  -------------  -------------------  ----------------")
        print(tabulate(df, showindex=False, headers=df.columns))
        print("------  -------------  -------------------  ----------------")
        print("\n")
        print("TOTAL MEMORY ALLOCATED FOR",self.name,":",total_mem)
        print("\n")

if __name__ == "__main__":
    with open('RunTimeManagement//test_code.c','r') as file:
        content = file.read()
        buffer = content.split()

    n = len(buffer)

    size = {'int':4,'float':4,'doub':8,'char':1,'bool':1}

    def computeStruct(buffer,i):
        mem = 0
        for candidate in range(i,n):
            c = buffer[candidate]
            if c == 'int' or c == 'float':
                mem += size[c]
            elif c == 'double':
                mem += size[c]
            elif c == 'char' or c == 'bool': 
                mem += size[c]
            elif c == '};':
                break
        mem += 2
        return mem

    def fillstruct_mem_dict(buffer):
        for candidate in range(n):
            c = buffer[candidate]

            if c == 'struct':
                size[buffer[candidate + 1]] = computeStruct(buffer,candidate)

            if '(' in c:
                break

    fillstruct_mem_dict(buffer)

    def findFuncIndex(name,buffer):
        start = 0
        end = 0
        for candidate in range(len(buffer)):
            c = buffer[candidate]

            if name in c:
                start = candidate
                break
        
        for i in range(start,len(buffer)):
            if buffer[i] == '}':
                end = i
                break
        return (start,end)
    

    def RunProgram(buffer):
        print("ALLOCATION:")
        CALL_STACK = Stack()

        main_index = findFuncIndex("main()",buffer)
        start,end = main_index[0],main_index[1]
        a = Function("main()")
        a.update(start,end,buffer)
        a.allocateMem()
        a.display()
        CALL_STACK.push(a)

        i = start + 1

        while i <= end:
            c = buffer[i]

            if '(' in c:
                name = c
                p = ""
                for k in name:
                    if k != '(':
                        p += k
                    else:
                        break

                s,e = findFuncIndex(p,buffer)

                func = Function(name[:-1])
                func.update(s,e,buffer)
                func.allocateMem()
                func.display()
                CALL_STACK.push(func)
            i += 1
        
        print("DEALLOCATION:\n")
        while CALL_STACK.top != -1:
            print("Now deallocating",CALL_STACK.pop().name)

                
    RunProgram(buffer)