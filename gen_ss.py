# Example usage: python3 gen_ss.py sqrt1111
import random
import in_form
import sys

default_swaps = [['0','w0'],['1','w1'],['0','w'],['1','w'],['I','J'],['1','I'],
         ['0','I'], ['I1','1'],['J','I1'],['K','I'],['K','1'],['I0','0'],
         ['I0','J'],['I0','X'],['I1','X'],['w0','X'],['w1','X'],['P','w0'],
         ['P','w1']]

def gen_swap_dict(state):
    '''determines swap location dictionary from state (represented as string)'''
    swap_dict = {}
    for i in range(len(state)):
        # check for ends of rows
        if (i+1) % rowl != 0:
            swap_dict[(i, i+1)] = state[i] in swaps[state[i+1]]
        # check for last row
        if i + rowl < len(state):
            swap_dict[(i, i+rowl)] = state[i] in swaps[state[i+rowl]]
    return swap_dict

def make_swap(state, swap):
    '''takes old state and swap and returns new state'''
    s = list(state)
    s[swap[0]], s[swap[1]] = s[swap[1]], s[swap[0]]
    return ''.join(s)

def pos_swaps(swap_dict):
    '''possible swaps from swap location dictionary'''
    return list({k:v for (k,v) in swap_dict.items() if v}.keys())

def update(n_state, prev_swap_list, swap):
    j, k = swap
    mut = []
    for i in [j, k]:
        if i % rowl != 0:
            mut.append((i-1, i))
        if (i+1) % rowl != 0:
            mut.append((i, i+1))
        if i + rowl < len(n_state):
            mut.append((i, i+rowl))
        if i - rowl >= 0:
            mut.append((i-rowl, i))
    new_swap_list = []
    for s in prev_swap_list:
        if s not in mut:
            new_swap_list.append(s)
    for s in mut:
        if n_state[s[0]] in swaps[n_state[s[1]]]:
            new_swap_list.append(s)
    return new_swap_list

def traverse(start, wj_d):
    unchecked = [start]
    statespace ={start:pos_swaps(gen_swap_dict(start))}
    while unchecked != []:
        for swap in statespace[unchecked[0]]:
            if swap in wj_d.keys():
                swap = wj_d[swap]
            n_state = make_swap(unchecked[0], swap)
            if n_state not in statespace:
                statespace[n_state] = update(n_state, statespace[unchecked[0]], swap)
                unchecked.append(n_state)
        del unchecked[0]
        if len(statespace) % 10000 == 0:
            print("States visited: %d" % len(statespace))
    return statespace

def hitting(start, i1, i2, n):
    output = {"HT":0}
    for i in range(n):
        state = start
        ht = 0
        ps = pos_swaps(gen_swap_dict(start))
        while state[i1] == 'w' or state[i2] == 'w':
            swap = random.choice(ps)
            state = make_swap(state, swap)
            ht += float(1)/len(ps)
            ps = update(state, ps, swap)
        if (state[i1], state[i2]) in output:
            output[(state[i1], state[i2])] += 1
        else:
            output[(state[i1], state[i2])] = 1
        output["HT"] += ht
        print(output)
    output["HT"] /= n
    return output

sp_map = in_form.get_species_map(default_swaps)
wj_d = in_form.wirejumps(sys.argv[1])
swaps = in_form.genswaps(default_swaps, sp_map)
for i in range(2, len(sys.argv)):
    filename = sys.argv[i]
    init_state, rowl = in_form.trans2in(filename, sp_map)
    ss = traverse(init_state, wj_d)
    in_form.trans2out(list(ss.keys()), filename)
    in_form.checkouts(filename, 0,1)#566, 799)
