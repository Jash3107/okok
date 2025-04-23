grammar={'E':['E+T','T'],'T':['T*F','F'],'F':['(E)','id']}
firsts={}
follow={}

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

def computeFollow(symbol):
    if symbol not in follow:
        follow[symbol]=set()
    for nt in grammar:
        for production in grammar[nt]:
            for i in range(len(production)):
                if production[i]==symbol:
                    if i+1<len(production):
                        nextSym=production[i+1]
                        if not isNonTerminal(nextSym):
                            follow[symbol].add(nextSym)
                        else:
                            computeFirst(nextSym)
                            follow[symbol].update(firsts[nextSym]-'#')
                            if '#' in firsts[nextSym]:
                                if symbol!=nt:
                                    computeFollow(nt)
                                    follow[symbol].update(follow[nt])
                    else:
                        if symbol!=nt:
                                    computeFollow(nt)
                                    follow[symbol].update(follow[nt])

computeFollow('E')
follow['E'].add('$')
computeFollow('T')
computeFollow('F')

print(follow)


                        



