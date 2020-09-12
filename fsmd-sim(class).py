# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 20:50:37 2020

@author: Paulo Lima
"""

import sys
from xml.dom import minidom
import time



#Variable initialization ---------------------------------------------------
class Gcd_xml:
    
    #This function returns a list of all state names 
    def get_states(self):
        state_names = self.df.getElementsByTagName('state')
        states = []
        for elem in state_names:
            states.append(elem.firstChild.data)
        return states
    
    
     #This function returns a string that contains the initial-state name
    def get_ini_state(self):     
        initial_state = self.df.getElementsByTagName('initialstate') 
        initial_state = initial_state[0].firstChild.data
        return initial_state                       
        
    
    #This function initializes the "inputs" 
    def ini_input(self):
        l=[]
        result = self.df.getElementsByTagName('input')
        for elem in result:
            l.append((elem.firstChild.data,0))
        return dict(l)

    def ini_var(self):
        l=[]
        result = self.df.getElementsByTagName('variable')
        for elem in result:
            l.append((elem.firstChild.data,0))
        return dict(l)
    
    
    #This function initializes "operations" 
    
    def ini_oper(self):
        l=[]
        result = self.df.getElementsByTagName('operation')
        for elem in result:
            name = elem.getElementsByTagName('name')
            name = name[0].firstChild.data
            expression = elem.getElementsByTagName('expression')
            expression = expression[0].firstChild.data
            l.append((name,expression))
        return dict(l)
        
    
    def ini_cond(self):
        l=[]
        result = self.df.getElementsByTagName('conditionlist')
        result = result[0].getElementsByTagName('condition')
        for elem in result:
            name = elem.getElementsByTagName('name')
            name = name[0].firstChild.data
            expression = elem.getElementsByTagName('expression')
            expression = expression[0].firstChild.data
            l.append((name,expression))
        return dict(l)
        
    
    
    #This function initializes the "fsdm" variable
    def ini_fsmd(self):
        fsmd=[]
        for elem in self.states:
        #elem represents each state
            statet = self.df.getElementsByTagName(elem)
             
            for node in statet:
            #node represents each transition inside a state 'elem'
                transitions = node.getElementsByTagName('transition')
                l=[]
                for node1 in transitions: 
                #node1 represents esch field inside a a transition 
                    condition = node1.getElementsByTagName('condition')
                    instruction = node1.getElementsByTagName('instruction')
                    nextstate = node1.getElementsByTagName('nextstate')
                    
                    condition = condition[0].firstChild.data
                    instruction = instruction[0].firstChild.data
                    nextstate = nextstate[0].firstChild.data
                    
                    d = dict((('condition',condition),('instruction',instruction),('nextstate',nextstate)))
                    l.append(d)
                              
            fsmd.append((elem,l))
        fsmd= dict(fsmd)
        return fsmd

    #This function initializes the "fsmd_stim" variable
    #def ini_fsmd_stim(stimuli_file):    
    
    
    def values(self):
        self.states = self.get_states()
        self.initial_state = self.get_ini_state()
        self.inputs = self.ini_input()
        self.variables = self.ini_var()
        self.operations = self.ini_oper()
        self.conditions = self.ini_cond()
        self.fsmd = self.ini_fsmd()    
  


#FUNCTIONS-------------------------------------------------------------------------

    def execute_setinput(self,operation):
        op = self.operations[operation].split(' ')
        if op[2] == 'var_A'or op[2] == 'var_b':
            self.variables[op[0]] = self.variables[op[2]] - self.variables[op[4]]
        else:
            self.variables[op[0]] = self.inputs[op[2]]

    


       
    

def main(a,b,c):
    #variables
    max_cycles = a #int(sys.argv[1])
    description_file = b #sys.argv[2]
    stimuli_file = c #sys.argv[3]
    obj = Gcd_xml()
    obj.df = minidom.parse(description_file)
    obj.values()
    
    #--------
    for i in range(max_cycles):
        obj.execute_setinput('A_minus_B')
    return obj.states,obj.initial_state,obj.inputs, obj.variables,obj.operations, obj.conditions


#if __name__ == '__main__' :
#    main()



