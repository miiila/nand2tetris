import sys

SYMBOL_TABLE = {
    "SP": 0x0000,
    "LCL": 0x0001,
    "ARG": 0x0002,
    "THIS": 0x0003,
    "THAT": 0x0004,
    "R0": 0x0000,
    "R1": 0x0001,
    "R2": 0x0002,
    "R3": 0x0003,
    "R4": 0x0004,
    "R5": 0x0005,
    "R6": 0x0006,
    "R7": 0x0007,
    "R8": 0x0008,
    "R9": 0x0009,
    "R10": 0x000a,
    "R11": 0x000b,
    "R12": 0x000c,
    "R13": 0x000d,
    "R14": 0x000e,
    "R15": 0x000f,
    "SCREEN": 0x4000,
    "KBD": 0x6000,
}

CURRENT_SYMBOL_ADDRESS = 0x0010;


def parse_line(line):
    # ignore comments and empty lines
    if line.startswith('//') or line == '':
        return None
    if line.startswith('@'):
        # return address
        return ('A', consume_line(line))
    if line.startswith('('):
        # return content of ()
        end = line.find(')')
        return ('LABEL', line[1:end])
    return ('C', consume_line(line))


def consume_line(line):
    # first space or new line terminates
    start = 0
    for i in range(0, len(line)):
        # check for comment or space
        if line[0] == '@':
            start = 1
        if line[i] == '/' and line[i+1] == '/' or line[i] == ' ':
            return line[start:i] 

    return line[start:i+1]



def handle_jmp(jmp):
    jmp_dict = {
        None :'000',
        'JGT':'001',
        'JEQ':'010',
        'JGE':'011',
        'JLT':'100',
        'JNE':'101',
        'JLE':'110',
        'JMP':'111'
    }

    return jmp_dict[jmp]

def handle_dest(dest_ins):
    dest = 0b000 
    if dest_ins is None:
        return format(dest,'03b')
    if 'M' in dest_ins:
        dest |= 1
    if 'D' in dest_ins:
        dest |= 2
    if 'A' in dest_ins:
        dest |= 4

    return format(dest,'03b')

def handle_comp(comp):
    comp_dict = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        'M': '1110000',
        '!D': '0001101',
        '!A': '0110001',
        '!M': '1110001',
        '-D': '0001111',
        '-A': '0110011',
        '-M': '1110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'M+1': '1110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'M-1': '1110010',
        'D+A': '0000010',
        'D+M': '1000010',
        'D-A': '0010011',
        'D-M': '1010011',
        'A-D': '0000111',
        'M-D': '1000111',
        'D&A': '0000000',
        'D&M': '1000000',
        'D|A': '0010101',
        'D|M': '1010101',
    }

    return comp_dict[comp]


def handle_a(ins):
    global CURRENT_SYMBOL_ADDRESS
    if not ins.isdigit():
        if ins not in SYMBOL_TABLE:
            SYMBOL_TABLE[ins] = CURRENT_SYMBOL_ADDRESS
            CURRENT_SYMBOL_ADDRESS += 1

        symbol = SYMBOL_TABLE[ins]
    else:
        symbol = ins

    return format(int(symbol), '016b')

def handle_c(ins):
    destComp, *jmp = ins.split(';')
    jmp = jmp[0] if jmp else None
    dest, *comp = destComp.split('=')
    if comp:
        comp = comp[0]
    else:
        comp = dest
        dest = None

    return '111'+handle_comp(comp)+handle_dest(dest)+handle_jmp(jmp)


def first_pass(lines):

    next_lines = []

    ins_count = 0;
    for line in lines:
        l = parse_line(line.strip())
        if l is not None:
            if l[0] is 'LABEL':
                SYMBOL_TABLE[l[1]] = ins_count
            else:
                next_lines.append(l)
                ins_count += 1

    return next_lines


def second_pass(lines):
    output = []

    for (insType, ins) in lines:
        if insType == 'A':
            output.append(handle_a(ins))
        elif insType == 'C':
            output.append(handle_c(ins))

    return output


file = sys.argv[1]
with open(file, 'r') as f:
    lines = f.readlines()


next_lines = first_pass(lines)
output = second_pass(next_lines)

with open(file.split('.')[0]+'.hack', 'w') as f:
    f.writelines('\n'.join(output))

