input_code = [
    "JOHN    START  0",
    "        USING  *, 15",
    "        L      1, FIVE",
    "        A      1, FOUR",
    "        ST     1, TEMP",
    "FOUR    DC     F '4'",
    "FIVE    DC     F '5'",
    "TEMP    DS     1F",
    "        END"
]

MOT = {
    "L": {"mnemonic": "L", "binary_opcode": "", "length": "000010", "format": "001"},
    "A": {"mnemonic": "A", "binary_opcode": "", "length": "000010", "format": "001"},
    "ST": {"mnemonic": "ST", "binary_opcode": "", "length": "000010", "format": "001"}
}

POT = {
    "START": {"pseudo_op": "START", "routine_address": ""},
    "USING": {"pseudo_op": "USING", "routine_address": ""},
    "DC": {"pseudo_op": "DC", "routine_address": ""},
    "DS": {"pseudo_op": "DS", "routine_address": ""},
    "END": {"pseudo_op": "END", "routine_address": ""}
}

symbol_table = {}
literal_table = []
LC = 0

# PASS 1
for line in input_code:
    parts = line.strip().split(maxsplit=2)

    label = ""
    opcode = ""
    operand = ""

    if len(parts) == 3:
        label, opcode, operand = parts
    elif len(parts) == 2:
        opcode, operand = parts
    elif len(parts) == 1:
        opcode = parts[0]

    # Handle START separately
    if opcode == "START":
        LC = int(operand)
        if label:
            symbol_table[label] = {"value": LC, "length": 1, "R/A": "R"}
        continue

    # If there's a label and it's not already in table, insert it
    if label and opcode != "START":
        # Handle DC specially — it’s both a symbol and a literal
        if opcode == "DC":
            symbol_table[label] = {"value": LC, "length": 4, "R/A": "R"}
            literal_table.append({
                "literal": operand,
                "value": LC,
                "length": 4,
                "R/A": "R"
            })
            LC += 4
            continue
        elif opcode == "DS":
            symbol_table[label] = {"value": LC, "length": 4, "R/A": "R"}
            LC += 4
            continue
        elif opcode in MOT:
            symbol_table[label] = {"value": LC, "length": 4, "R/A": "R"}
            LC += 4
            continue
        elif opcode in POT:
            symbol_table[label] = {"value": LC, "length": 4, "R/A": "R"}
            continue

    # Handle instruction without label
    if opcode in MOT:
        LC += 4
    elif opcode == "DC":
        # If no label, still treat as literal
        literal_table.append({
            "literal": operand,
            "value": LC,
            "length": 4,
            "R/A": "R"
        })
        LC += 4
    elif opcode == "DS":
        LC += 4

# PASS 2 — BASE TABLE
base_table = [{"available": "N", "contents": ""} for _ in range(16)]
base_table[15]["available"] = "Y"

# OUTPUT
print("\nMACHINE OPERATION TABLE (MOT)")
print("{:<10} {:<15} {:<15} {:<15}".format("Mnemonic", "Binary Opcode", "Instr Length", "Instr Format"))
for m in MOT.values():
    print("{:<10} {:<15} {:<15} {:<15}".format(m['mnemonic'], m['binary_opcode'], m['length'], m['format']))

print("\nPSEUDO OPERATION TABLE (POT)")
print("{:<10} {:<20}".format("Pseudo Op", "Routine Address"))
for p in POT.values():
    print("{:<10} {:<20}".format(p['pseudo_op'], p['routine_address']))

print("\nSYMBOL TABLE")
print("{:<10} {:<10} {:<10} {:<10}".format("Symbol", "Value", "Length", "R/A"))
for sym, val in symbol_table.items():
    print("{:<10} {:<10} {:<10} {:<10}".format(sym, val['value'], val['length'], val['R/A']))

print("\nLITERAL TABLE")
print("{:<10} {:<10} {:<10} {:<10}".format("Literal", "Value", "Length", "R/A"))
for lit in literal_table:
    print("{:<10} {:<10} {:<10} {:<10}".format(lit['literal'], lit['value'], lit['length'], lit['R/A']))

print("\nBASE TABLE")
print("{:<10} {:<10}".format("Available", "Contents"))
for base in base_table:
    print("{:<10} {:<10}".format(base['available'], base['contents']))
