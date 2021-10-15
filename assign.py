#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
# Sri Venkata Sai Anoop Bulusu 2000761292
# Shriya Reddy Pulagam         2000770412
# Srinivas Yashvanth Valavala  2000756858
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import itertools
import random
from copy import deepcopy

#To load data from input file 
def load_people(filename):
    l = []
    with open(filename, "r") as file:
        for line in file:
            l.append(line.split())
    return l

#Assign variables according to data pulled from input file
def assign_variables(list_of_input):
    people_name = []
    want_to_work = dict()
    dont_want_to_work = dict()
    no_of_people = 0
    no_of_people = len(list_of_input)
    for i in range(len(list_of_input)):
        people_name.append(list_of_input[i][0])
        want_to_work[list_of_input[i][0]] = list_of_input[i][1].split('-')
        dont_want_to_work[list_of_input[i][0]] = list_of_input[i][2].split(',')
    return no_of_people,people_name,want_to_work,dont_want_to_work

#To arrange persons to list of one,two and three groups
def arrange_into_teams(people_name,dont_want_to_work):
    teams1 = []
    teams2 = []
    teams3 = []
    for i in range(len(people_name)):
        teams1.append(people_name[i])
        for j in range(i+1,len(people_name)):
            if (people_name[j] in dont_want_to_work[people_name[i]]) or (people_name[i] in dont_want_to_work[people_name[j]]):
                continue
            else:
                teams2.append([people_name[i],people_name[j]])
    check_team = []
    for k in range(len(people_name)):
        
        for l in range(k+1,len(people_name)):
            if (people_name[l] in dont_want_to_work[people_name[k]]) or (people_name[k] in dont_want_to_work[people_name[l]]):
                continue
            else:
                check_team = ([people_name[k],people_name[l]])
                for m in range(l+1,len(people_name)):
                    if (people_name[m] in dont_want_to_work[check_team[0]] or people_name[m] in dont_want_to_work[check_team[1]]) or (check_team[0]in dont_want_to_work[people_name[m]] or check_team[1] in dont_want_to_work[people_name[m]]):#checktwoway
                        continue
                    else:
                        teams3.append([people_name[k],people_name[l],people_name[m]])
    return teams1,teams2,teams3

#To find total cost
def total_cost(batch,cost,want_to_work):
    return(cost_of_teams(batch,cost)+cost_for_not_same_group(batch,want_to_work,cost) + cost_not_assigned(batch,want_to_work,cost))


def cost_of_teams(batch, cost):
    cost = 5*len(batch)
    return cost

def cost_for_not_same_group(batch,want_to_work,cost):
    for group in batch:
        for people in group:
            if len(want_to_work[people]) != len(group):
                cost = cost+2 
    return cost

def cost_not_assigned(batch,want_to_work,cost):
    people_work = []
    for group in batch:
        for people in group:
            people_work = want_to_work[people]
            for i in range(1,len(people_work)):
                if people_work[i] not in group and people_work[i] != 'xxx' and people_work[i] != 'zzz':
                    cost = cost+3
    return cost

#Finding combination of teams based on itertools 
def combination_of_batches(people_name):
    len_of_people=len(people_name)
    possible_group = []
    while len_of_people > 0:
        for poss_comb in itertools.combinations_with_replacement([1,2,3],len_of_people):
            if max(poss_comb)<=3 and sum(poss_comb) == len(people_name):
                possible_group.append(poss_comb)
        len_of_people = len_of_people-1
    return possible_group

def solver(input_file):
    list = load_people(input_file)
    no_of_people,people_name,want_to_work,dont_want_to_work = assign_variables(list)
    single_team, double_team, triple_team = arrange_into_teams(people_name,dont_want_to_work)
    possible_states = combination_of_batches(people_name)
    cost = 0
    cost_min = 9999
    while True:
        single_team_dup = deepcopy(single_team)
        double_team_dup = deepcopy(double_team)
        triple_team_dup = deepcopy(triple_team)
        random.shuffle(single_team_dup)
        random.shuffle(double_team_dup)
        random.shuffle(triple_team_dup)
        for possible_batch in possible_states:
            single_team_dup1 = deepcopy(single_team_dup)
            double_team_dup1 = deepcopy(double_team_dup)
            triple_team_dup1 = deepcopy(triple_team_dup)
            visited_names = []
            batch = [[] for x in range(len(possible_batch))]
            assigned_groups = []
            for i in range(len(possible_batch)):
                if possible_batch[i] == 1:
                    for name in single_team_dup1:
                        gr_1 = name
                        if gr_1 in visited_names:
                            continue
                        else:
                            visited_names.append(gr_1)
                            b = 0
                            for j in range(len(batch)):
                                if gr_1 in batch[j]:
                                    b = 1
                                    break
                            if b == 0:
                                batch[i].append(gr_1)
                                break
                            else:
                                continue
                elif possible_batch[i] == 2:
                    for name in double_team_dup1:
                        gr_2 = name
                        if gr_2 in visited_names:
                            continue
                        else:
                            visited_names.append(gr_2)
                            b = 0
                            for j in range(len(batch)):
                                if (gr_2[0] in batch[j]) or (gr_2[1] in batch[j]):
                                    b = 1
                                    break
                                    
                            if b == 0:
                                batch[i].extend(gr_2)
                                break
                            else:
                                continue
                if possible_batch[i] == 3:
                    for name in triple_team_dup1:
                        gr_3 = name
                        if gr_3 in visited_names:
                            continue
                        else:
                            visited_names.append(gr_3)
                            b = 0
                            for j in range(len(batch)):
                                if (gr_3[0] in batch[j]) or (gr_3[1]  in batch[j]) or (gr_3[2] in batch[j]):
                                    b = 1
                                    break
                            if b == 0:
                                batch[i].extend(gr_3)
                                break
                            else:
                                continue
            
            c = total_cost(batch,cost, want_to_work)

            group_length = 0

            for groups in batch:
                group_length = group_length+len(groups)
            if group_length == no_of_people:
                for groups in batch:
                    assigned_groups.append('-'.join(groups))
                if c < cost_min:
                    yield({"assigned-groups": assigned_groups, "total-cost" : c})
                    cost_min = c
                


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
