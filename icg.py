import re

def precedence(op):
    return {'=': 0, '+': 1, '-': 1, '*': 2, '/': 2}.get(op, -1)

def is_operator(token):
    return token in ['+', '-', '*', '/', '=']

def to_postfix(tokens):
    stack = []
    output = []
    for token in tokens:
        if is_operator(token):
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)
    while stack:
        output.append(stack.pop())
    return output

def generate_quadruples(expr):
    expr = expr.replace(" ", "")
    lhs, rhs = expr.split("=")

    tokens = re.findall(r'[A-Za-z_]\w*|\d+|[-+*/=]', rhs)
    postfix = to_postfix(tokens)

    stack = []
    quadruples = []
    temp_count = 1

    for token in postfix:
        if not is_operator(token):
            stack.append(token)
        else:
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = f"t{temp_count}"
            quadruples.append((token, arg1, arg2, result))
            stack.append(result)
            temp_count += 1

    # Final assignment
    final_result = stack.pop()
    quadruples.append(('=', final_result, '-', lhs))
    return quadruples

# Example usage
expr = "a = b + c * d"
quadruples = generate_quadruples(expr)

print("Quadruples:\n")
print("(op, arg1, arg2, result)")
for quad in quadruples:
    print(quad)
