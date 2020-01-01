#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


def fuzz_Mem_Func(var, typeOfMf, lst):
    '''
    returns Upper membership values.
    
    keyword arguments:
    
    var -- x range of variable 
    typeOfMf -- type of membershi function
    lst -- list of values provided
    '''
    if typeOfMf == 'trimf':
        return fuzz.trimf(var,lst)
    elif typeOfMf == 'gaussmf':
        mean, sigma = lst
        return fuzz.gaussmf(var, mean, sigma)
    elif typeOfMf == 'gauss2mf':
        mean1, sigma1, mean2, sigma2 = lst
        return fuzz.gauss2mf(var, mean1, sigma1, mean2, sigma2)
    elif typeOfMf == 'trapmf':
        return fuzz.trapmf(var, lst)
    elif typeOfMf == 'gbellmf':
        a,b,c = lst
        return fuzz.gbellmf(var, a, b, c)


def fuzz_Inputs(x_var, var):
    '''
    returns the list membership values along the range
    and the list of linguistic terms chosen.
    
    keyword arguments:
    
    x_var -- x range of the variable var
    var -- variable name
    '''

#   input linguistic terms for a linguistic variable. 
    lst = input(f'Enter the fuzzy inputs for variable {var}:').split(' ')

    In_ = [] #list to store the membership values.
    
    for i in range(len(lst)):
        typeofMf = input(f'Enter the type of membership function for {lst[i]} {var}:')
        
        '''The input format here for membership values.
        
        ex: trapziodal func: [a b c d]
        traingular func: [a b c]
        '''
        varType = [type(x_var[0])(x) for x in input(f"Enter the numbers for {lst[i]} {var}:").split(' ')]
        
        varmf = fuzz_Mem_Func(x_var, typeofMf, varType)
        In_.append(varmf)
    
    lstoflst = [In_, lst]
    return lstoflst


def fuzz_plot_mf(x_var, var_, var_types, varName):
    '''
    plots the membership graph for variable varName.
    
    keyword argument:
    
    varName -- name of the variable
    x_var -- x range of variable varName
    var_ -- list of membership values
    var_types -- list storing the linguistic terms
    '''
    print(f'The following plot shows the {varName}')
    fig, ax = plt.subplots(figsize=(8, 3))

    for i in range(len(var_)):
        ax.plot(x_var, var_[i], linewidth=1.5, label=var_types[i])
    ax.set_title(varName)
    ax.legend()


def fuzz_make_rules(var1_types, var2_types):
    '''
    returns a list with decided rules.
    
    keyword arguments:
    
    var1_types -- linguistic terms of first variable
    var2_types -- linguistic terms of second variable
    '''
    
    rule_lst = []
    for i in range(len(var1_types)):
        rule_ = []
        for j in range(len(var2_types)):
            rule_.append(int(input(f'Enter the number corresponding to the above fitness level menu for rule {var1_types[i]} and {var2_types[j]}: ')))
        rule_lst.append(rule_)
    return rule_lst


def fuzz_Interplot_mem(x_var, lst, singleton_value):
    '''
    Does the inter plotting bw singleton value and the membership value.
    
    keywords arguments:
    
    x_var -- x range of values of a variable
    var -- list of membership values
    singleton_value -- input value
    '''
    memvalue = []
    for i in range(len(lst)):
        memvalue.append(fuzz.interp_membership(x_var, lst[i], singleton_value))

    return memvalue


def fuzz_rule(row_memvalue, col_memvalue, output_, rule_lst):
    '''
    Maps the membership values of the antecedents with the consequent on the basis of decided rules.
    
    keyword arguments:
    
    row_memvalue -- membership values of a antecedent along the row
    col_memvalue -- membership values of a antecedent along the column
    output_ -- membership values of the consequent 
    rule_lst -- list containing the decided rules
    '''
    rule = [] #list stroing maped value of membership functions
    output_used = [] #list of membership values of the consequent used acc. to the decided rules
    for i in range(len(row_memvalue)):
        for j in range(len(col_memvalue)):
            fitness_used.append(output_[rule_lst[i][j] - 1])
            rule.append(np.fmin(np.fmin(row_memvalue[i], col_memvalue[j]), output_[rule_lst[i][j] - 1]))

    return [rule, output_used]


def fuzz_plot_outputMf(x_var, rule, output_used):
    '''
    plot output membership function at a given singleton value.
    
    keyword arguments:
    
    x_var -- x range of variable
    rule -- mapped rules for memberships
    output_used -- type of linguistic terms of output used based on the rules decided
    '''
    zerolike = np.zeros_like(x_var)
    fig, ax0 = plt.subplots(figsize=(8, 3))

    for i in range(len(rule)):
        ax0.fill_between(x_var, zerolike, rule[i], facecolor='orange', alpha=0.7)
        ax0.plot(x_var, output_used[i], linewidth=0.5,linestyle='--')

    ax0.set_title('Output membership activity')

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    return


def fuzz_aggregation(rule):
     '''
    aggregates the rules.
    
    keyword arguments:
    
    rule --  maped rule for membership
    '''
    l = len(rule) - 1
    npfmax = np.fmax(rule[l - 1], rule[l])
    for i in range(len(rule) - 2):
        l = (len(rule) - 1) - (i + 1)
        npfmax = np.fmax(rule[l - 1], npfmax)

    return npfmax


def fuzz_defuzz(x_var, R_combined):
    '''
    defuzzifies based on the aggregated rules.
    
    keyword arguments:
    
    x_var -- x range of variable
    R_combined_ -- aggregated rules for membership values
    '''
    output = fuzz.defuzz(x_var, R_combined, 'centroid')
    output_activation = fuzz.interp_membership(x_var, R_combined, output)
    lst = [output, output_activation]
    return lst


def fuzz_output(x_var, var, output, output_activation, R_combined):
    '''
    plots the ouput value along with the centroid.
    
    keyword arguments:
    
    x_var -- x range of the variable
    var -- membership values of the consequent
    output -- centroid value
    output_activation -- membership value of centroid value
    R_combined -- aggregated rules for membership functions 
    '''
    fig, ax0 = plt.subplots(figsize=(8, 3))
    zerolike = np.zeros_like(x_var)
    for i in range(len(var)):
        ax0.plot(x_var, var[i], linewidth=0.5, linestyle='--', )
    ax0.fill_between(x_var, zerolike, R_combined, facecolor='Orange', alpha=0.7)
    ax0.plot([output, output], [0, output_activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Aggregated membership and result (line)')

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    print(f'Output = {output}')






