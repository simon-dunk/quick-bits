b1 = "00000010010100110100000000100000" # R-Type
b2 = "10001101001010000000010010110000" # LW
b3 = "00000010010100111000100000100010" # R-Type
b4 = "00001000000000000000000000000000" # J-Type
b5 = "10101101001010000000000000000000" # SW
b6 = "00010001000010010000000000000000" # BEQ
b7 = "00010101000010010000000000000000" # BNE
b8 = "00000001001010100100000000100000"
b9 = "10101101011010010001100000000000"

# Register mapping for MIPS
registers = {
    "00000": "$zero", "00001": "$at", "00010": "$v0", "00011": "$v1", "00100": "$a0", "00101": "$a1", "00110": "$a2", "00111": "$a3",
    "01000": "$t0", "01001": "$t1", "01010": "$t2", "01011": "$t3", "01100": "$t4", "01101": "$t5", "01110": "$t6", "01111": "$t7",
    "10000": "$s0", "10001": "$s1", "10010": "$s2", "10011": "$s3", "10100": "$s4", "10101": "$s5", "10110": "$s6", "10111": "$s7",
    "11000": "$t8", "11001": "$t9", "11010": "$k0", "11011": "$k1", "11100": "$gp", "11101": "$sp", "11110": "$fp", "11111": "$ra"
}

def bit_breaker(sizes, binary_str):
    bits = []
    index = 0
    for size in sizes:
        bits.append(binary_str[index:index + size])
        index += size
    return bits

def interpret_mips_instruction(bit_segments):
    opcode = bit_segments[0]
    mips_instructions = {
        "000000": ("R-type (Register format)", {
            'RegDst': '1', 'ALUOp': '10', 'ALUSrc': '0', 'MemtoReg': '0', 'RegWrite': '1', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '0'
        }),
        "000010": ("J-type (Jump instruction)", {
            'RegDst': 'x', 'ALUOp': 'xx', 'ALUSrc': 'x', 'MemtoReg': 'x', 'RegWrite': '0', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '1'
        }),
        "100011": ("LW (Load Word)", {
            'RegDst': '0', 'ALUOp': '00', 'ALUSrc': '1', 'MemtoReg': '1', 'RegWrite': '1', 'MemRead': '1', 'MemWrite': '0', 'Branch': '0', 'Jump': '0'
        }),
        "101011": ("SW (Store Word)", {
            'RegDst': 'x', 'ALUOp': '00', 'ALUSrc': '1', 'MemtoReg': 'x', 'RegWrite': '0', 'MemRead': '0', 'MemWrite': '1', 'Branch': '0', 'Jump': '0'
        }),
        "000100": ("BEQ (Branch if Equal)", {
            'RegDst': 'x', 'ALUOp': '01', 'ALUSrc': '0', 'MemtoReg': 'x', 'RegWrite': '0', 'MemRead': '0', 'MemWrite': '0', 'Branch': '1', 'Jump': '0'
        }),
        "000101": ("BNE (Branch if Not Equal)", {
            'RegDst': 'x', 'ALUOp': '01', 'ALUSrc': '0', 'MemtoReg': 'x', 'RegWrite': '0', 'MemRead': '0', 'MemWrite': '0', 'Branch': '1', 'Jump': '0'
        }),
    }
    instruction_info = mips_instructions.get(opcode, ("Unknown Instruction", {}))
    return instruction_info

def get_rtype_function(funct):
    """Map the funct field to the actual R-type operation"""
    funct_map = {
        "100000": "ADD", 
        "100010": "SUB", 
        "100100": "AND", 
        "100101": "OR", 
        "101010": "SLT"
    }
    return funct_map.get(funct, "Unknown Function")

def generate_assembly(instruction_type, bit_segments):
    """Generate the assembly format for R-type and other instructions"""
    if instruction_type == "R-type (Register format)":
        funct = bit_segments[5]
        operation = get_rtype_function(funct)
        rd = registers.get(bit_segments[3], "$unknown")
        rs = registers.get(bit_segments[1], "$unknown")
        rt = registers.get(bit_segments[2], "$unknown")
        return f"{operation} {rd}, {rs}, {rt}"
    elif instruction_type == "LW (Load Word)":
        rt = registers.get(bit_segments[2], "$unknown")
        rs = registers.get(bit_segments[1], "$unknown")
        return f"lw {rt}, 0({rs})"
    elif instruction_type == "SW (Store Word)":
        rt = registers.get(bit_segments[2], "$unknown")
        rs = registers.get(bit_segments[1], "$unknown")
        return f"sw {rt}, 0({rs})"
    elif instruction_type == "BEQ (Branch if Equal)" or instruction_type == "BNE (Branch if Not Equal)":
        rs = registers.get(bit_segments[1], "$unknown")
        rt = registers.get(bit_segments[2], "$unknown")
        return f"{instruction_type.split()[0].lower()} {rs}, {rt}, label"
    elif instruction_type == "J-type (Jump instruction)":
        # J-type: address is in the last segment (bit_segments[1])
        address = bit_segments[1]
        return f"j {address}"  # Generate jump instruction with address
    else:
        return "Unknown instruction"

def print_mips_decoding(sizes, binary_str):
    space_string = "     "
    bit_segments = bit_breaker(sizes, binary_str)
    instruction, control_signals = interpret_mips_instruction(bit_segments)
    
    print("\n|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|")
    print("Original Binary String:")
    print(space_string + binary_str)
    print("\nBreakdown:")
    for i, (size, segment) in enumerate(zip(sizes, bit_segments)):
        print(f"{space_string}Segment {i + 1} ({size} bits): {segment}")
    
    print("\nDecoded Instruction:")
    print(space_string + instruction)
    
    print("\nControl Signals:")
    for signal, value in control_signals.items():
        print(f"{space_string}{signal}: {value}")
    
    assembly = generate_assembly(instruction, bit_segments)
    print("\nAssembly:")
    print(space_string + assembly)
    
    print("|______________________________________________|\n")

sizes = [6, 5, 5, 5, 5, 6]
print_mips_decoding(sizes, b1)
print_mips_decoding(sizes, b2)
print_mips_decoding(sizes, b3)
print_mips_decoding(sizes, b4)
print_mips_decoding(sizes, b5)
print_mips_decoding(sizes, b6)
print_mips_decoding(sizes, b7)
print_mips_decoding(sizes, b8)
print_mips_decoding(sizes, b9)
