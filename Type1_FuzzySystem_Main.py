 # if __name__ == '__main__':


'''
input format:
x -- the starting value of the range.
y -- the upper bound of the range
z -- the incrementation value (the difference two values of the range)
'''
x, y, z = [int(x) for x in input("Enter the range of weight:").split(' ')]
x_weight = np.arange(x, y, z)

x, y, z = [float(x) for x in input("Enter the range of height:").split(' ')]
x_height = np.arange(x, y, z)

x, y, z = [int(x) for x in input("Enter the range of fitnes level:").split(' ')]
x_fitnessLevel = np.arange(x, y, z)


'''
w -- 2D tuple containing seperate UMF and LMF of weight(here).
w_types -- list containg the linguistic terms for weight(here).
'''
w_, w_types = fuzz_Inputs(x_weight, 'weight')

h_,h_types = fuzz_Inputs(x_height, 'height')

f_,f_types = fuzz_Inputs(x_fitnessLevel, 'fitness level')


'''
Ploting the membership values for each of antecedent and consequent
'''
fuzz_plot_mf(x_weight, w_, w_types, 'Weight')
fuzz_plot_mf(x_height, h_, h_types, 'Height')
fuzz_plot_mf(x_fitnessLevel, f_,f_types, 'Fitness Level')


'''
Displays the list of linguistic terms of the consequent, corresponding to a value.
'''
for i in range(len(f_types)):
    print(f'{i+1}) {f_types[i]}')


'''
rule_lst -- list of rules decided
'''
rule_lst = fuzz_make_rules(w_types, h_types)


weight = int(input('Enter Value for weight:'))
height = float(input('Enter value for height:'))


'''
x_memvalue -- membership value at a particular single value for the antecedent x(weight and height here).
'''
w_memvalue = fuzz_Interplot_mem(x_weight, w_, weight)
h_memvalue = fuzz_Interplot_mem(x_height, h_, height)


'''
rule -- maped rule for membership values.
fitness_used -- list of fitness values decided based the rule_lst(to be used for ploting)
'''
rule, fitness_used = fuzz_rule(w_memvalue, h_memvalue, f_, rule_lst)


fuzz_plot_outputMf(x_fitnessLevel, rule, fitness_used)


'''
R_combined -- aggregated rule for membership values.
'''
R_combined = fuzz_aggregation(rule)


'''
fitnessLevel -- output value(centroid value)
fitness_activation -- corresponding membership value of output
'''
fitnessLevel, fitness_activation = fuzz_defuzz(x_fitnessLevel, R_combined)


fuzz_output(x_fitnessLevel, f_, fitnessLevel, fitness_activation, R_combined)
