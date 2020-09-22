#!/usr/bin/env python3

import sys
import xmltodict

print("Welcome to the FSMD simulator! - Version ?? - Designed by ??")

if len(sys.argv) < 3:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) >4):
    print('Too many arguments.')
    sys.exit(-1)

iterations = int(sys.argv[1])

#Parsing the FSMD description file
with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())

#Parsing the stimuli file
fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())

print("\n--FSMD description--")

#
# Description:
# The 'states' variable of type 'list' contains the list of all states names.
#
states = fsmd_des['fsmddescription']['statelist']['state']
print("States:")
for state in states:
    print('  ' + state)
#
# Description:
# The 'initial_state' variable of type 'string' contains the initial_state name.
#
initial_state = fsmd_des['fsmddescription']['initialstate']
print("Initial state:")
print('  ' + initial_state)

#
# Description:
# The 'inputs' variable of type 'dictionary' contains the list of all inputs
# names and value. The default value is 0.
#
inputs = {}
if(fsmd_des['fsmddescription']['inputlist'] is None):
    inputs = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
        # One element
        inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
    else:
        # More elements
        for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
            inputs[input_i] = 0
print("Inputs:")
for input_i in inputs:
    print('  ' + input_i)

#
# Description:
# The 'variables' variable of type 'dictionary' contains the list of all variables
# names and value. The default value is 0.
#
variables = {}
if(fsmd_des['fsmddescription']['variablelist'] is None):
    variables = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
        # One element
        variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
    else:
        # More elements
        for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
            variables[variable] = 0
print("Variables:")
for variable in variables:
    print('  ' + variable)

#
# Description:
# The 'operations' variable of type 'dictionary' contains the list of all the
# defined operations names and expressions.
#
operations = {}
if(fsmd_des['fsmddescription']['operationlist'] is None):
    operations = {}
    #No elements
else:
    for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
        if type(operation) is str:
            # Only one element
            operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                fsmd_des['fsmddescription']['operationlist']['operation']['expression']
            break
        else:
            # More than 1 element
            operations[operation['name']] = operation['expression']
print("Operations:")
for operation in operations:
    print('  ' + operation + ' : ' + operations[operation])

#
# Description:
# The 'conditions' variable of type 'dictionary' contains the list of all the
# defined conditions names and expressions.
#
conditions = {}
if(fsmd_des['fsmddescription']['conditionlist'] is None):
    conditions = {}
    #No elements
else:
    for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
        if type(condition) is str:
            #Only one element
            conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
            break
        else:
            #More than 1 element
            conditions[condition['name']] = condition['expression']
print("Conditions:")
for condition in conditions:
    print('  ' + condition + ' : ' + conditions[condition])

#
# Description:
# The 'fsmd' variable of type 'dictionary' contains the list of dictionaries,
# one per state, with the fields 'condition', 'instruction', and 'nextstate'
# describing the FSMD transition table.
#
fsmd = {}
for state in states:
    fsmd[state] = []
    for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:
        if type(transition) is str:
            #Only one element
            fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
            break
        else:
            #More than 1 element
            fsmd[state].append({'condition' : transition['condition'],
                                'instruction' : transition['instruction'],
                                'nextstate' : transition['nextstate']})
print("FSMD transitions table:")
for state in fsmd:
    print('  ' + state)
    for transition in fsmd[state]:
        print('    ' + 'nextstate: ' + transition['nextstate'] + ', condition: ' + transition['condition'] + ', instruction: ' + transition['instruction'])


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionary 'inputs'
#
def execute_setinput(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)
    return


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionaries 'variables' and 'inputs'
#
def execute_operation(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    variables[target] = eval(expression, {'__builtins__': None}, merge_dicts(variables, inputs))
    return


#
# Description:
# This function executes a list of operations passed as string and spaced by
# a single space using the expression defined in the dictionary 'operations'
#
def execute_instruction(instruction):
    if instruction == 'NOP' or instruction == 'nop':
        return
    instruction_split = instruction.split(' ')
    for operation in instruction_split:
        execute_operation(operations[operation])
    return


#
# Description:
# This function evaluates a Python compatible boolean expressions of
# conditions passed as string using the conditions defined in the variable 'conditions'
# and using the operands stored in the dictionaries 'variables' and 'inputs
# It returns True or False
#
def evaluate_condition(condition):
    if condition == 'True' or condition=='true' or condition == 1:
        return True
    if condition == 'False' or condition=='false' or condition == 0:
        return False
    condition_explicit = condition
    for element in conditions:
        condition_explicit = condition_explicit.replace(element, conditions[element])
    #print('----' + condition_explicit)
    return eval(condition_explicit, {'__builtins__': None}, merge_dicts(variables, inputs))


#
# Description:
# Support function to merge two dictionaries.
#
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


#######################################
# Start to simulate
print('\n---Start simulation---')


# Setting up the environment we will work in.

# State stores the state the sfmd is in.
state = initial_state
# Cycle stores the cycle the sfmd is in.
cycle, max_cycle = 0, iterations
# End state is the state we want to break out of.
end_state = ""
if 'fsmdstimulus' in fsmd_stim and 'endstate' in fsmd_stim['fsmdstimulus']:
    end_state = fsmd_stim['fsmdstimulus']['endstate'] 

# Getting the stimulus for each cycle.
stim_per_cicle = dict()
for c in range(max_cycle + 1):
    stim_per_cicle[c] = []

# Extract stimulus from fsmd_stim.
# It's a litle bit tricky as if there is a single
# stimulus, then it's a dict, otherwise it's a list
# of dicts.
if 'fsmdstimulus' not in fsmd_stim:
    fsmd_stim['fsmdstimulus'] = {}
if 'setinput' not in fsmd_stim['fsmdstimulus']:
    fsmd_stim['fsmdstimulus']['setinput'] = []
fsmd_stim = fsmd_stim['fsmdstimulus']['setinput'] 
def ExtractStim(elem):
    stim_per_cicle[int(elem['cycle'])].append(elem['expression'])
if type(fsmd_stim) == list:
    for elem in fsmd_stim:
        ExtractStim(elem)
else:
    ExtractStim(fsmd_stim)

# Prints the current state of the simulation.
def PrintStateInfo():
    print(f"Cycle #{cycle}:")
    print(f"  Current state: {state}")
    print(f"  Current variables:")
    for var in variables:
        print(f"    {var}: {variables[var]}")
    print(f"  Current inputs:")
    for var in inputs:
        print(f"    {var}: {inputs[var]}")

# Prints information in the valid transition.
def PrintTransitionInfo(transition):
    print(f"  Matching transition found:")
    print(f"    Condition: {transition['condition']}")
    print(f"    Instruction: {transition['instruction']}")
    print(f"    Next State: {transition['nextstate']}")

while cycle < max_cycle:
    for stim in stim_per_cicle[cycle]:
        execute_setinput(stim)

    PrintStateInfo()

    # If state = end_state, we need to exit.
    if state == end_state:
        print(f"  Exited because the current state ({state}) is the End State!")
        break

    # Iterating through the transitions available to find a matching one.
    for transition in fsmd[state]:
        # This is the valid transition
        if evaluate_condition(transition['condition']):
            PrintTransitionInfo(transition)
            execute_instruction(transition['instruction'])
            state = transition['nextstate']
            # We changed state so we need to get out of the loop
            # to avoid undefined behaviour.
            break
    else:
        # If we get here it means that no condition matched.
        # This state is illegal.
        print("Unexpected state!")
        exit()

    # Increment cycle.
    cycle += 1


######################################
######################################

print('\n---End of simulation---')

#
# Description:
# This is a code snippet used to update the inputs values according to the
# stimuli file content. You can see here how the 'fsmd_stim' variable is used.
#
'''
try:
    if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
        for setinput in fsmd_stim['fsmdstimulus']['setinput']:
            if type(setinput) is str:
                #Only one element
                if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                    execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                break
            else:
                #More than 1 element
                if int(setinput['cycle']) == cycle:
                    execute_setinput(setinput['expression'])
except:
    pass
'''

#
# Description:
# This is a code snipppet used to check the endstate value according to the
# stimuli file content. You can see here how the 'fsmd_stim' variable is used.
#
'''
try:
    if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
        if state == fsmd_stim['fsmdstimulus']['endstate']:
            print('End-state reached.')
            repeat = False
except:
    pass
'''
