# Open the NFA_Input_2.txt file
file = open("NFA_Input_2.txt", "r")

number_line = 0

alphabet = states = final_states = []
first_state = ""
# NFA_dict is nested dictionary for store NFA information
NFA_dict = {}

# Read file line by line and store NFA information(alphabet, states, ...)
for line in file:
    if number_line == 0:
        # Alphabet of NFA
        alphabet = line.strip().split(" ")
    elif number_line == 1:
        # All states in NFA
        states = line.strip().split(" ")
    elif number_line == 2:
        # First state in NFA
        first_state = line.strip()
    elif number_line == 3:
        # All final states in NFA
        final_states = line.strip().split(" ")
    else:
        str_line_strip = line.strip().split(" ")
        # Example for line_strip : q0 a q1
        current_state = str_line_strip[0]
        # In this example current_state = q0
        tape = str_line_strip[1]
        if tape in alphabet:
            tape = str_line_strip[1]
        else:
            tape = "lambda"
        # This if condition denote tape is λ or no! if tape = λ, store "lambda"

        next_state = str_line_strip[2]
        # In this example next_state = q1

        # This if condition for store (current_state and tape and next_state) in nested dictionary
        if not current_state in NFA_dict:
            NFA_dict[current_state] = {tape: {next_state}}
        else:
            if tape in NFA_dict[current_state].keys():
                old_values = NFA_dict[current_state][tape]
                new_values = {next_state}
                total_values = old_values.union(new_values)
                NFA_dict[current_state][tape] = total_values
            else:
                NFA_dict[current_state][tape] = {next_state}
    number_line += 1

    '''
    This function return all lambda closure in state (s)
    for example (q0 lambda q1) and (q1 lambda q2)
    lambda_closure(q0) return {q1,q2}
    '''


def lambda_closure(s):
    result = {}
    for x in NFA_dict[s].keys():
        if x == "lambda":
            result = NFA_dict[s][x].union({s})
            for ls in NFA_dict[s][x]:
                result = result.union(lambda_closure(ls))
    return result


DFA_current_state = []
DFA_tape = []
DFA_next_state = []
start = {first_state}
# ADD start state in DFA from NFA
DFA_current_state.append(start)

# This loop for build DFA from NFA_dict
for state in DFA_current_state:
    for t in alphabet:
        next_state_set = {}
        for s in state:
            if t in NFA_dict[s].keys():
                next_state_set = NFA_dict[s][t].union(next_state_set)
                for ls in NFA_dict[s][t]:
                    next_state_set = next_state_set.union(lambda_closure(ls))
            if 1 == 1:
                if not lambda_closure(s) is None:
                    for ls in lambda_closure(s):
                        if t in NFA_dict[ls].keys():
                            next_state_set = NFA_dict[ls][t].union(next_state_set).union(lambda_closure(ls))
        DFA_tape.append(t)
        DFA_next_state.append(next_state_set)
    for ns in DFA_next_state:
        if not ns in DFA_current_state:
            DFA_current_state.append(ns)

DFA_alphabet = alphabet
DFA_states = DFA_current_state
DFA_first_state = first_state
DFA_final_states = []

# This loop for build final_states in DFA
for state in DFA_states:
    for s in state:
        if s in final_states:
            if not state in DFA_final_states:
                DFA_final_states.append(state)
        else:
            for ls in lambda_closure(s):
                if ls in final_states:
                    if not state in DFA_final_states:
                        DFA_final_states.append(state)

# write in DFA_Output_2.txt
f = open("DFA_Output_2.txt", "w")
for alp in DFA_alphabet:
    f.write(alp + " ")
f.write("\n")
for state in DFA_states:
    # Use Replace for remove ' from states in set
    state = (str(state)).replace("\'", "")
    f.write(state + " ")
f.write("\n")
f.write(DFA_first_state + "\n")
for fState in DFA_final_states:
    fState = (str(fState)).replace("\'", "")
    f.write(fState + " ")
f.write("\n")
for i in range(0, len(DFA_tape)):
    DFA_cState = str(DFA_current_state[int(i / len(alphabet))]).replace("\'", "")
    tape = str(DFA_tape[i])
    DFA_nState = str(DFA_next_state[i]).replace("\'", "")
    f.write(DFA_cState + " " + tape + " " + DFA_nState + "\n")
