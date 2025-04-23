import re

# Define keywords and symbols
keywords = {
    'int', 'float', 'char', 'if', 'else', 'while', 'for', 'do', 'return',
    'break', 'continue', 'void', 'static', 'switch', 'case', 'default',
    'include', 'define', 'struct', 'typedef'
}

symbols = set('(){}[];,+-*/%=<>&|!^~?:.#')

def remove_comments(code):
    # Remove single-line and multi-line comments
    code = re.sub(r'//.*', '', code) 
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def lexical_analyzer(code):
    code = remove_comments(code)

    # Match header files like <stdio.h>
    headers = re.findall(r'<\w+\.h>', code)
    for header in headers:
        code = code.replace(header, '')  # Remove from code temporarily

    tokens = re.findall(r'\#\w+|[A-Za-z_]\w*|\d+|[^\sA-Za-z0-9_]', code)

    print("\nLexical Analysis Output:")
    for token in tokens:
        if token.startswith('#'):
            print(f"{token} : Preprocessor Directive")
        elif token in keywords:
            print(f"{token} : Keyword")
        elif token.isdigit():
            print(f"{token} : Number")
        elif token in symbols:
            print(f"{token} : Symbol")
        elif re.match(r'[A-Za-z_]\w*', token):
            print(f"{token} : Identifier")
        else:
            print(f"{token} : Unknown")

    for header in headers:
        print(f"{header} : Header File")

# ---- Example usage ----
code = '''
#include <stdio.h>
// This is a comment
int main() {
    int a = 10;
    float pi = 3.14;
    return 0;
}
'''

lexical_analyzer(code)
