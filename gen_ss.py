# Example usage: python3 gen_ss.py sqrt1111



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

def update_sd(n_state, prev_swap_dict, swap):
    new_swap_dict = prev_swap_dict.copy()
    mut = [[swap[i], swap[i]-1, swap[i]-rowl] for i in range(2)]
    mut = [i for i in mut[0] + mut[1] if i>=0]
    for i in mut:
        if (i+1) % rowl != 0:
            new_swap_dict[(i, i+1)] = n_state[i] in swaps[n_state[i+1]]
        if i + rowl < len(n_state):
            new_swap_dict[(i, i+rowl)] = n_state[i] in swaps[n_state[i+rowl]]
    return new_swap_dict

def traverse(start):
    unchecked = [start]
    statespace = {start:gen_swap_dict(start)}
    while unchecked != []:
        for swap in pos_swaps(statespace[unchecked[0]]):
            n_state = make_swap(unchecked[0], swap)
            if n_state not in statespace.keys():
                statespace[n_state] = update_sd(n_state, statespace[unchecked[0]], swap)
                unchecked.append(n_state)
        del unchecked[0]
    return statespace

filename = sys.argv[1]
sp_map = in_form.get_species_map(default_swaps)
init_state, swaps, rowl = in_form.trans2in(default_swaps, filename, sp_map)
ss = traverse(init_state)
in_form.trans2out(list(ss.keys()), filename, sp_map)
