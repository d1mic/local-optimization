from basicBlock import BasicBlock
import libraries.yacc as yacc
import optParser

def fetchInstructions(fileName):
  
    try: 
        with open(fileName, 'r') as f:
            instructions = []
            for line in f:
                inst = line.rstrip('\n').rstrip(' ')
                if(inst):
                    instructions.append(inst)
        return instructions
    except IOError as e:
        exit(e)

def getLeaders(instructions):
    leaders = []
    leaders.append(instructions[0])
    
    for i in range(len(instructions)):
        if(instructions[i].__contains__("GOTO")):
            
            if((i+1) != len(instructions)):
                leaders.append(instructions[i+1])
            try:
                index = int(instructions[i].split(' ')[-1])
                leaders.append(instructions[index-1])
            except ValueError as e:
                exit(e)

    return list(set(leaders))

def instanceBasicBlocks(instructions):
    leaders = getLeaders(instructions)
    basicBlocks = []

    for instruction in instructions:
        if leaders.__contains__(instruction):
            basicBlocks.append(BasicBlock(instruction))
        basicBlocks[-1].addInstruction(instruction)

    return basicBlocks

def toCode(instr):
    if(instr[0] == "assign"):
        if(len(instr[3]) == 3 ):
            [operator , left, right ] = instr[3]
            return instr[1] + " " + instr[2] + " " + str(left[1]) + " " +  operator +  " " + str(right[1])
        elif(len(instr[3]) == 2):
            return instr[1] + " " + instr[2] + " " + str(instr[3][1])

def neutralElimination(tmp):
    if(len(tmp[3]) == 3 ):    
        [ operator, left, right ] = tmp[3]
        res = tmp[3]
        if operator == '+':
            if left[1] == 0:
                res = right
            elif right[1] == 0:
                res = left
        elif operator == '*':
            if left[1] == 0 or right[1] == 0:
                res = ('const', 0)
            elif left[1] == 1:
                res = right
            elif right[1] == 0:
                res = right  
        return (tmp[0],tmp[1],tmp[2],res)
    else:
        return tmp

def constantFolding(tmp):
    if(len(tmp[3]) == 3 ): 
        [operator, left, right ] = tmp[3]
        res = tmp[3]
        if(left[0] == "const" and right[0] == "const"):
            if operator == "+":
                res = left[1] + right[1]
            elif operator == '-':
                res = left[1] - right[1]
            elif operator == '*':
                res = left[1] * right[1]
            elif operator == '/':
                res = left[1] / right[1]
            return (tmp[0],tmp[1],tmp[2],("const", res))
        else:
            return tmp
    else:
        return tmp
   

def optimizeBlock(block):

    blockInstr = []
    blockInstr = block.getInstructions()

    for i in range(len(blockInstr)):
        tmp = yacc.parse(blockInstr[i])
        if(tmp[0] == "assign"):
            optimized = constantFolding(neutralElimination(tmp))
            optCode = toCode(optimized)
            blockInstr[i] = optCode
    return block


def main():
    fileName = 'test/test_examples/test1.txt'
    instructions = fetchInstructions(fileName)
    blocks = instanceBasicBlocks(instructions)
    for block in blocks:
        print optimizeBlock(block)
    
if __name__ == "__main__":
    main()