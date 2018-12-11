def get_species_map(swaps):
    # takes species with multiple char and maps it to a single char name
    # doesn't work for >7 species to be reassigned
    sp = []
    for pair in swaps:
        for s in pair:
            sp.append(s)
    sp = set(sp)
    i = 2
    sp_map = {'z':'z','n':'n'}
    for s in sp:
        if len(s) > 1:
            sp_map[s] = str(i)
            sp_map[str(i)] = s
            i += 1
        else:
            sp_map[s] = s
    return sp_map

def translate(sl, sp_map):
    for i in range(len(sl)):
        for j in range(len(sl[0])):
            sl[i][j] = sp_map[sl[i][j]]
    return sl

def genswaps(swaps):
    '''Turns list of swaps into dictionary of rules'''
    rulesdict = {"n":[],"z":[]}
    for swap in swaps:
        for sp in swap:
            if sp not in rulesdict.keys():
                rulesdict[sp] = []
                for rule in swaps:
                    if sp in rule:
                        rulesdict[sp] += [x for x in rule if x != sp]
    return rulesdict

def trans2in(swaps, filename, sp_map):
    tswaps = genswaps(translate(swaps, sp_map))
    f = open('circuits/'+filename, 'r')
    state = [line.strip().split() for line in f.readlines()]
    rowl = len(state[0])
    tstate = translate(state, sp_map)
    tstate = ''.join([''.join(l) for l in tstate])
    f.close()
    return tstate, tswaps, rowl

def trans2out(states, filename):
    tstates = [s+'\n' for s in states]
    f = open('statespaces/'+filename, 'w+')
    f.writelines(tstates)
    f.close()
    print("Wrote to file!")

def display(filename, sp_map, rowl):
    f = open('statespaces/'+filename, 'r')
    states = f.readlines()
    f.close()
    f = open('statespaces/%spretty' % filename, 'w+')
    for state in states:
        state = list(state)
        for i in range(len(state)):
            if (i+1) % rowl == 0:
                f.write(" ".join(state[i-rowl+1:i+1]) + '\n')
        f.write('\n')
    f.close()
    print("Made pretty file!")

def wirejumps(filename):
    f = open('jumps/'+filename, 'r')
    wj_d = {}
    for line in f.readlines():
        [a, b, c, d] = line.strip().split()
        [a, b, c, d] = [int(a), int(b), int(c), int(d)]
        wj_d[(min(a,b), max(a,b))] = (a,d)
        wj_d[(min(c,d), max(c,d))] = (a,d)
    return wj_d

def checkouts(filename, i1, i2):
    f = open('statespace/'+filename, 'r')
    output = {}
    for line in f.readlines():
        if (line[i1], line[i2]) in output:
            output[(line[i1], line[i2])] += 1
        else:
            output[(line[i1], line[i2])] = 1
    f.close()
    f = open('outputs/'+filename, 'r')
    f.write(str(output))
    f.close()
