import csv
import numpy as np
import sys

def shift_votes(votes_by_choice, ivoter):
    voter_votes = votes_by_choice[:,ivoter]
    unique_votes = np.unique(voter_votes)
    update_dict = {}
    for i, vote in enumerate(unique_votes):
        update_dict[int(vote)] = i + 1

    for i in range(len(voter_votes)):
        voter_votes[i] = update_dict[voter_votes[i]]


if len(sys.argv) != 3:
    print('Usage:\npython stv.py <csv file with votes> <number of voters>')
    sys.exit(1)

nvoters = int(sys.argv[2])
choices = []
votes_by_choice = []

with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for row in reader:
        choices.append(row[0])
        votes_by_choice.append(list(map(int, row[1:nvoters + 1])))

votes_by_choice = np.array(votes_by_choice)
print(votes_by_choice)

votes_to_win = nvoters / 2

while True:
    for i in range(nvoters):
        shift_votes(votes_by_choice, i)

    # print('Shifted votes:')
    # print(votes_by_choice)

    weight_of_1 = []
    for i in range(nvoters):
        weight_of_1.append(1 / np.count_nonzero(votes_by_choice[:,i] == 1))
    weight_of_1 = np.array(weight_of_1)

    current_total = []
    for i, choice in enumerate(choices):
        votes = sum((votes_by_choice[i,:] == 1) * weight_of_1)
        current_total.append((i, float(votes)))

    sorted_total = list(sorted(current_total, key=lambda x: -x[1]))

    print('\nCurrent top:')
    for ichoice, votes in sorted_total[:3]:
        print(f"{choices[ichoice]}: {votes:.2f}")

    if sorted_total[0][1] >= votes_to_win:
        break

    worst_choice = None
    worst_1s = nvoters
    worst_top_vote = 1
    for ichoice in range(len(choices)):
        votes = votes_by_choice[ichoice,:]
        num_1s = current_total[ichoice][1]
        top_vote = np.min(votes)
        if num_1s < worst_1s or (num_1s == worst_1s and top_vote > worst_top_vote):
            worst_choice = ichoice
            worst_1s = num_1s
            worst_top_vote = top_vote

    assert worst_choice is not None

    print(f'\nEliminating "{choices[worst_choice]}" with votes  {votes_by_choice[worst_choice,:]} ({worst_1s:.2f} votes 1, highest vote {worst_top_vote})')
    choices = choices[:worst_choice] + choices[worst_choice + 1:]
    votes_by_choice = np.delete(votes_by_choice, worst_choice, axis=0)
