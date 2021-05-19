# An Assembler for Hack language
#%% File Handling
import sys # command-line arguments library

# expect a single argument in input with the name of the file
input_source = sys.argv[1]

output_file = 'output.hack'
#%% # Define hash tables for C-instruction conversion
comp_field = {}
comp_field['0']   = '0101010'
comp_field['1']   = '0111111'
comp_field['-1']  = '0111010'
comp_field['D']   = '0001100'
comp_field['A']   = '0110000'
comp_field['!D']  = '0001101'
comp_field['!A']  = '0110001'
comp_field['-D']  = '0001111'
comp_field['-A']  = '0110011'
comp_field['D+1'] = '0011111'
comp_field['A+1'] = '0110111'
comp_field['D-1'] = '0001110'
comp_field['A-1'] = '0110010'
comp_field['D+A'] = '0000010'
comp_field['D-A'] = '0010011'
comp_field['A-D'] = '0000111'
comp_field['D&A'] = '0000000'
comp_field['D|A'] = '0010101'
comp_field['M']   = '1110000'
comp_field['!M']  = '1110001'
comp_field['-M']  = '1110011'
comp_field['M+1'] = '1110111'
comp_field['M-1'] = '1110010'
comp_field['D+M'] = '1000010'
comp_field['D-M'] = '1010011'
comp_field['M-D'] = '1000111'
comp_field['D&M'] = '1000000'
comp_field['D|M'] = '1010101'

dest_field = {
              ''  : '000',
              'M' : '001',
              'D' : '010',
              'MD': '011',
              'A' : '100',
              'AM': '101',
              'AD': '110',
              'AMD':'111',
             }

jump_field = {
              ''    : '000',
              'JGT' : '001',
              'JEQ' : '010',
              'JGE' : '011',
              'JLT' : '100',
              'JNE' : '101',
              'JLE' : '110',
              'JMP' :'111',
             }

predefined_symbols = {
                      'R0':0,
                      'R1':1,
                      'R2':2,
                      'R3':3,
                      'R4':4,
                      'R5':5,
                      'R6':6,
                      'R7':7,
                      'R8':8,
                      'R9':9,
                      'R10':10,
                      'R11':11,
                      'R12':12,
                      'R13':13,
                      'R14':14,
                      'R15':15,
                      'SCREEN':16384,
                      'KBD':24576,
                      'SP':0,
                      'LCL':1,
                      'ARG':2,
                      'THIS':3,
                      'THAT':4
                      }

#%% Parser
def cleanWhitespace(curr_line):
    '''Clear white-space: Remove empty lines, remove comments'''
    curr_line.strip()
    if curr_line == '':
        return ''
    if '//' in curr_line: # commented line
        curr_line = curr_line.split('//') # creates 2 segments
        curr_line = curr_line[0] # Empty line in case of pure comment, instruction otherwise

    # Strip all spaces between words to minimize translation dictionary size
    curr_line = ''.join(curr_line.split(' '))
    return curr_line.strip()

def parseCinstruction(input):
    ''' 
    C-instructions have 3 fields: dest, comp, jump
    Split instruction into 3 fields and convert each field based on hashed symbol table
    EITHER dest ('=' omitted) or jump (';' omitted) field may be empty, NOT BOTH
    '''
    if '=' in input: # split by '=' yields dest, comp
        dest, comp = input.split('=')
    else:
        dest = ''
        comp = input
    if ';' in input: # split by ';' yields comp, jump
        compt, jump = comp.split(';')
    else:
        compt = comp
        jump = ''
    # print(' DEST ' + dest + ' COMP ' + compt + ' JUMP ' + jump)
    parsedInstruction = '111'
    parsedInstruction += comp_field[compt]
    parsedInstruction += dest_field[dest]
    parsedInstruction += jump_field[jump]
    return parsedInstruction

def parseAinstruction(input):
    ''' 
    A-instructions have @ as first symbol
    Can be either predefined symbol or memory address
    If memory address (== purely numeric), convert the following number to binary, append zeros
    else replace with lookup from symbolic table
    '''
    value = input[1:]  # split line after @
    if value.isnumeric():
        a_instruction = "{0:b}".format(int(value)) #TODO: Replace with custom atoi
    else:
        key = predefined_symbols.get(value, 'None')
        a_instruction = "{0:b}".format(key)
    a_instruction = '0'*(16 - len(a_instruction)) + a_instruction # append missing zeros to fill field 
    return a_instruction

#%% State Machine
symbolless_code = []
machine_code = [] # Store translated lines to this, write to file at end

# LEXER: Clean whitespace, add symbols to predefined tables
with open(input_source, 'r') as source:

    # Whitespace removal pass
    no_whitespace_code = []
    for curr_line in source:
        curr_line = cleanWhitespace(curr_line) # remove white space before parsing
        if curr_line == '':
            continue
        no_whitespace_code.append(curr_line)

    # Label extraction pass
    no_label_code = []
    for curr_line in no_whitespace_code:
        if '(' in curr_line: # code label
            linenumber = len(no_label_code)
            predefined_symbols[curr_line[1:-1]] = linenumber
            continue # do not emit code for label
        no_label_code.append(curr_line)

    # Variable memory allocation pass
    variable_assignment = 16
    for curr_line in no_label_code:
        if '@' in curr_line: # variable if non-numeric, non-existent in symbol table
            addr = curr_line[1:]
            if addr.isnumeric() != True: # not memory address
                value = predefined_symbols.get(addr, None)
                if value == None: # undefined variable
                    predefined_symbols[addr] = variable_assignment # assign location from 16 onwards
                    variable_assignment += 1
        symbolless_code.append(curr_line)

# PARSER
for curr_line in symbolless_code:
    if curr_line[0] == '@': # A-instruction
        machine_code.append(parseAinstruction(curr_line))
    else: # C-instruction
        machine_code.append(parseCinstruction(curr_line))

# CODE OPTIMIZER = TODO

# EMMITTER
with open(output_file, 'w') as destination:
    for inst in machine_code:
        destination.write(inst + '\n')
