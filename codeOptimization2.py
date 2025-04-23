def constant_propagation(lines):
    var_values = {}
    optimized = []

    for line in lines:
        var, rhs = line.split('=')
        var = var.strip()
        rhs = rhs.strip()

        # Replace known constants
        rhs_vars = [token for token in rhs.split() if token.isidentifier()]
        for v in rhs_vars:
            if v in var_values:
                rhs = rhs.replace(v, var_values[v])

        # Try evaluating the RHS if possible
        try:
            rhs = str(eval(rhs))
        except:
            pass

        optimized.append(f"{var} = {rhs}")

        if rhs.isdigit():
            var_values[var] = rhs

    return optimized


def dead_code_elimination(lines):  # Changed to match function call
    optimized = []
    rhs_vars = []
    for line in lines:
        var, rhs = line.split('=')
        var = var.strip()
        rhs = rhs.strip()
        rhs_vars += [token for token in rhs.split() if token.isidentifier()]
    for line in lines:
        var, rhs = line.split('=')
        var = var.strip()
        rhs = rhs.strip()
        if var in rhs_vars:
            optimized.append(f"{var} = {rhs}")  # Fixed formatting to match the input
    return optimized


# ✅ Test input
input_code = [
    'a = z',
    'b = x + y',
    'c = a + b',
    'd = c + d'
]

# 🔁 Run optimization
res = constant_propagation(input_code)
final = dead_code_elimination(res)  # Now matches the function name

# 📤 Output
print("Optimized Code:")
for line in final:
    print(line)