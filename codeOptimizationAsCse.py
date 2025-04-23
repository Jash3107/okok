def algebraic_simplify(expr):
    var, rhs = expr.split('=')
    var = var.strip()
    rhs = rhs.strip()

    # Simplify known algebraic identities
    if '+ 0' in rhs or '0 +' in rhs:
        rhs = rhs.replace('+ 0', '').replace('0 +', '')
    elif '* 1' in rhs or '1 *' in rhs:
        rhs = rhs.replace('* 1', '').replace('1 *', '')
    elif '* 0' in rhs or '0 *' in rhs:
        rhs = '0'
    elif '- 0' in rhs:
        rhs = rhs.replace('- 0', '')
    elif '/ 1' in rhs:
        rhs = rhs.replace('/ 1', '')

    return f"{var} = {rhs.strip()}"


def common_subexpression_elimination(code_lines):
    optimized = []
    expr_map = {}         # rhs -> lhs
    var_to_exprs = {}     # var -> set of exprs that depend on it

    for line in code_lines:
        simplified = algebraic_simplify(line)
        var, rhs = simplified.split('=')
        var = var.strip()
        rhs = rhs.strip()

        # If RHS is already computed and all its variables are still valid
        if rhs in expr_map:
            optimized.append(f"{var} = {expr_map[rhs]}")
        else:
            # Save expression
            expr_map[rhs] = var
            optimized.append(f"{var} = {rhs}")

            # Track variables used in RHS
            used_vars = [token for token in rhs.split() if token.isidentifier()]
            for v in used_vars:
                var_to_exprs.setdefault(v, set()).add(rhs)

        # Invalidate any expressions that depend on this variable
        if var in var_to_exprs:
            for expr in var_to_exprs[var]:
                expr_map.pop(expr, None)
            var_to_exprs[var].clear()

    return optimized


input_code = [
    "a = b + c",
    "d = b + c",      # d = a  ✅ (common subexpression)
    "b = 2",          # Invalidate all exprs that depend on b
    "e = b + c"
]

# --- Optimize ---
optimized_code = common_subexpression_elimination(input_code)

# --- Output ---
print("Optimized Code:\n")
for line in optimized_code:
    print(line)
