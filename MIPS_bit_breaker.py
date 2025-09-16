#!/usr/bin/env python3
"""
MIPS Instruction Decoder - Enhanced Bit Breaker
Automatically detects instruction types and provides comprehensive decoding
"""

# Test instructions
b1 = "00000010010100110100000000100000"  # R-Type ADD
b2 = "10001101001010000000010010110000"  # LW
b3 = "00000010010100111000100000100010"  # R-Type SUB
b4 = "00001000000000000000000000000000"  # J-Type
b5 = "10101101001010000000000000000000"  # SW
b6 = "00010001000010010000000000000000"  # BEQ
b7 = "00010101000010010000000000000000"  # BNE
b8 = "00000001001010100100000000100000"  # R-Type ADD
b9 = "10101101011010010001100000000000"  # SW
b10 = "011111111111100000110000101101100101010111110010"

# Enhanced register mapping for MIPS
registers = {
    "00000": "$zero", "00001": "$at",   "00010": "$v0",   "00011": "$v1",
    "00100": "$a0",   "00101": "$a1",   "00110": "$a2",   "00111": "$a3",
    "01000": "$t0",   "01001": "$t1",   "01010": "$t2",   "01011": "$t3",
    "01100": "$t4",   "01101": "$t5",   "01110": "$t6",   "01111": "$t7",
    "10000": "$s0",   "10001": "$s1",   "10010": "$s2",   "10011": "$s3",
    "10100": "$s4",   "10101": "$s5",   "10110": "$s6",   "10111": "$s7",
    "11000": "$t8",   "11001": "$t9",   "11010": "$k0",   "11011": "$k1",
    "11100": "$gp",   "11101": "$sp",   "11110": "$fp",   "11111": "$ra"
}

def bit_breaker(sizes, binary_str):
    """Break binary string into segments of specified sizes"""
    bits = []
    index = 0
    for size in sizes:
        if index + size <= len(binary_str):
            bits.append(binary_str[index:index + size])
            index += size
        else:
            bits.append(binary_str[index:])  # Get remaining bits
            break
    return bits

def detect_instruction_type(binary_str):
    """Automatically detect MIPS instruction type and return appropriate field sizes"""
    opcode = binary_str[:6]
    
    if opcode == "000000":
        # R-Type: opcode(6) + rs(5) + rt(5) + rd(5) + shamt(5) + funct(6)
        return "R-Type", [6, 5, 5, 5, 5, 6], ["opcode", "rs", "rt", "rd", "shamt", "funct"]
    elif opcode in ["000010", "000011"]:
        # J-Type: opcode(6) + address(26)
        return "J-Type", [6, 26], ["opcode", "address"]
    else:
        # I-Type: opcode(6) + rs(5) + rt(5) + immediate(16)
        return "I-Type", [6, 5, 5, 16], ["opcode", "rs", "rt", "immediate"]

def get_instruction_info(opcode, funct=None):
    """Get detailed instruction information based on opcode and funct"""
    instruction_map = {
        "000000": {  # R-Type instructions
            "name": "R-Type",
            "functions": {
                "100000": ("ADD", "Add"),
                "100010": ("SUB", "Subtract"), 
                "100100": ("AND", "Bitwise AND"),
                "100101": ("OR", "Bitwise OR"),
                "101010": ("SLT", "Set Less Than"),
                "000000": ("SLL", "Shift Left Logical"),
                "000010": ("SRL", "Shift Right Logical"),
                "001000": ("JR", "Jump Register")
            },
            "control": {'RegDst': '1', 'ALUOp': '10', 'ALUSrc': '0', 'MemtoReg': '0', 
                       'RegWrite': '1', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '0'}
        },
        "000010": ("J", "Jump", {
            'RegDst': 'X', 'ALUOp': 'XX', 'ALUSrc': 'X', 'MemtoReg': 'X', 
            'RegWrite': '0', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '1'
        }),
        "000011": ("JAL", "Jump and Link", {
            'RegDst': '2', 'ALUOp': 'XX', 'ALUSrc': 'X', 'MemtoReg': '2', 
            'RegWrite': '1', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '1'
        }),
        "100011": ("LW", "Load Word", {
            'RegDst': '0', 'ALUOp': '00', 'ALUSrc': '1', 'MemtoReg': '1', 
            'RegWrite': '1', 'MemRead': '1', 'MemWrite': '0', 'Branch': '0', 'Jump': '0'
        }),
        "101011": ("SW", "Store Word", {
            'RegDst': 'X', 'ALUOp': '00', 'ALUSrc': '1', 'MemtoReg': 'X', 
            'RegWrite': '0', 'MemRead': '0', 'MemWrite': '1', 'Branch': '0', 'Jump': '0'
        }),
        "000100": ("BEQ", "Branch if Equal", {
            'RegDst': 'X', 'ALUOp': '01', 'ALUSrc': '0', 'MemtoReg': 'X', 
            'RegWrite': '0', 'MemRead': '0', 'MemWrite': '0', 'Branch': '1', 'Jump': '0'
        }),
        "000101": ("BNE", "Branch if Not Equal", {
            'RegDst': 'X', 'ALUOp': '01', 'ALUSrc': '0', 'MemtoReg': 'X', 
            'RegWrite': '0', 'MemRead': '0', 'MemWrite': '0', 'Branch': '1', 'Jump': '0'
        }),
        "001000": ("ADDI", "Add Immediate", {
            'RegDst': '0', 'ALUOp': '00', 'ALUSrc': '1', 'MemtoReg': '0', 
            'RegWrite': '1', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '0'
        }),
        "001100": ("ANDI", "AND Immediate", {
            'RegDst': '0', 'ALUOp': '11', 'ALUSrc': '1', 'MemtoReg': '0', 
            'RegWrite': '1', 'MemRead': '0', 'MemWrite': '0', 'Branch': '0', 'Jump': '0'
        })
    }
    
    if opcode == "000000" and funct:
        r_type_info = instruction_map["000000"]
        if funct in r_type_info["functions"]:
            op, desc = r_type_info["functions"][funct]
            return op, desc, r_type_info["control"]
        else:
            return "UNKNOWN", "Unknown R-Type", r_type_info["control"]
    elif opcode in instruction_map:
        return instruction_map[opcode]
    else:
        return "UNKNOWN", "Unknown Instruction", {}

def generate_assembly(inst_type, bit_segments, field_names):
    """Generate assembly code from decoded instruction"""
    if inst_type == "R-Type":
        opcode, rs, rt, rd, shamt, funct = bit_segments
        operation, desc, _ = get_instruction_info(opcode, funct)
        
        rs_reg = registers.get(rs, f"${int(rs, 2)}")
        rt_reg = registers.get(rt, f"${int(rt, 2)}")
        rd_reg = registers.get(rd, f"${int(rd, 2)}")
        
        if operation in ["SLL", "SRL"]:  # Shift operations
            shamt_val = int(shamt, 2)
            return f"{operation.lower()} {rd_reg}, {rt_reg}, {shamt_val}"
        elif operation == "JR":
            return f"jr {rs_reg}"
        else:
            return f"{operation.lower()} {rd_reg}, {rs_reg}, {rt_reg}"
            
    elif inst_type == "J-Type":
        opcode, address = bit_segments
        operation, desc, _ = get_instruction_info(opcode)
        addr_val = int(address, 2) * 4  # Word-aligned address
        return f"{operation.lower()} 0x{addr_val:08x}"
        
    elif inst_type == "I-Type":
        opcode, rs, rt, immediate = bit_segments
        operation, desc, _ = get_instruction_info(opcode)
        
        rs_reg = registers.get(rs, f"${int(rs, 2)}")
        rt_reg = registers.get(rt, f"${int(rt, 2)}")
        imm_val = int(immediate, 2) if immediate[0] == '0' else int(immediate, 2) - (1 << 16)  # Sign extend
        
        if operation in ["LW", "SW"]:
            return f"{operation.lower()} {rt_reg}, {imm_val}({rs_reg})"
        elif operation in ["BEQ", "BNE"]:
            return f"{operation.lower()} {rs_reg}, {rt_reg}, {imm_val}"
        elif operation in ["ADDI", "ANDI"]:
            return f"{operation.lower()} {rt_reg}, {rs_reg}, {imm_val}"
        else:
            return f"{operation.lower()} {rt_reg}, {rs_reg}, {imm_val}"
    
    return "Unknown instruction format"

def print_mips_decoding(binary_str):
    """Main function to decode and display MIPS instruction"""
    
    # Auto-detect instruction type and get field information
    inst_type, sizes, field_names = detect_instruction_type(binary_str)
    bit_segments = bit_breaker(sizes, binary_str)
    
    # Get instruction details
    if inst_type == "R-Type":
        operation, description, control_signals = get_instruction_info(bit_segments[0], bit_segments[5])
    else:
        operation, description, control_signals = get_instruction_info(bit_segments[0])
    
    # Generate assembly
    assembly = generate_assembly(inst_type, bit_segments, field_names)
    
    # Pretty print results
    print("╔" + "═" * 70 + "╗")
    print(f"║ MIPS Instruction Decoder - {inst_type:<45} ")
    print("╠" + "═" * 70 + "╣")
    print(f"║ Binary: {binary_str:<55} ")
    print(f"║ Hex:    0x{int(binary_str, 2):08X}{' ' * 47} ")
    print("╠" + "═" * 70 + "╣")
    
    # Field breakdown
    print("║ Field Breakdown:" + " " * 52 + "")
    for i, (field, segment, size) in enumerate(zip(field_names, bit_segments, sizes)):
        decimal_val = int(segment, 2)
        if field in ["rs", "rt", "rd"] and segment in registers:
            reg_name = registers[segment]
            print(f"║   {field:<8} ({size:2}b): {segment} = {decimal_val:3} = {reg_name:<12} ")
        else:
            print(f"║   {field:<8} ({size:2}b): {segment} = {decimal_val:<15} ")
    
    print("╠" + "═" * 70 + "╣")
    print(f"║ Operation: {operation} - {description:<47} ")
    print(f"║ Assembly:  {assembly:<55} ")
    
    if control_signals:
        print("╠" + "═" * 70 + "╣")
        print("║ Control Signals:" + " " * 52 + "")
        # Split control signals into two columns for better formatting
        signals = list(control_signals.items())
        for i in range(0, len(signals), 2):
            left = f"{signals[i][0]}: {signals[i][1]}"
            right = f"{signals[i+1][0]}: {signals[i+1][1]}" if i+1 < len(signals) else ""
            print(f"║   {left:<32} {right:<32} ")
    
    print("╚" + "═" * 70 + "╝")
    print()

def main():
    """Main execution function"""
    print("🔧 MIPS Instruction Decoder - Enhanced Bit Breaker")
    print("=" * 72)
    print()
    
    instructions = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]
    
    for i, instruction in enumerate(instructions, 1):
        print(f"Instruction {i}:")
        print_mips_decoding(instruction)

if __name__ == "__main__":
    main()
