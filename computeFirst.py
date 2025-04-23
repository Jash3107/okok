grammar={'E':['E+T','T'],'T':['T*F','F'],'F':['(E)','id']}
firsts={}


def isNonTerminal(ch):
    return ch.isupper()

def computeFirst(symbol):
    if symbol not in firsts:
        firsts[symbol]=set()
    for production in grammar.get(symbol,[]):
        firstCh=production[0]
        if firstCh=='#':
            firsts[symbol].add('#')
        if not isNonTerminal(firstCh):
            if isNonTerminal(production[1]):
                firsts[symbol].add(firstCh)
            else:
                firsts[symbol].add(production)
        else:
            if firstCh!=symbol:
                computeFirst(firstCh)
                for f in firsts[firstCh]:
                    firsts[symbol].add(f)

computeFirst('E')
computeFirst('T')
computeFirst('F')
print(firsts)


