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

def generate_triples(expr):
    expr = expr.replace(" ", "")
    lhs, rhs = expr.split("=")

    tokens = re.findall(r'[A-Za-z_]\w*|\d+|[-+*/=]', rhs)
    postfix = to_postfix(tokens)

    stack = []
    triples = []

    for token in postfix:
        if not is_operator(token):
            stack.append(token)
        else:
            arg2 = stack.pop()
            arg1 = stack.pop()

            # If arg is an index (int), we keep it as is, otherwise just the variable
            if isinstance(arg1, int):
                arg1_ref = f"({arg1})"
            else:
                arg1_ref = arg1
            if isinstance(arg2, int):
                arg2_ref = f"({arg2})"
            else:
                arg2_ref = arg2

            triples.append((token, arg1_ref, arg2_ref))
            stack.append(len(triples) - 1)

    # Final assignment
    final_ref = f"({stack.pop()})" if isinstance(stack[-1], int) else stack.pop()
    triples.append(('=', final_ref, '-', lhs))
    return triples

# Example usage
expr = "a = b + c * d"
triples = generate_triples(expr)

print("Triples:\n")
print("(op, arg1, arg2)")
for i, triple in enumerate(triples):
    print(f"{i}: {triple}")
