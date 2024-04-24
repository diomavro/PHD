import csv
import pandas as pd
import os 
from constants import directory
from functions import create_dictionary_action, save_to_csv, run_decision_tree, build_decision_tree_from_csv

available_actions = ['Are there moral facts?', 'Are the moral facts natural? ', 'action3']

'''
user_dict = create_dictionary_action(available_actions)
print(user_dict)

csv_filename = '_user_dictionary.csv'
save_to_csv(user_dict, csv_filename)
print(f'Dictionary saved to {csv_filename}')
'''
# Save the decision tree to a CSV file
with open('_decision_tree.csv', 'w', newline='') as file:
    fieldnames = ['question', 'answers', 'follow_ups']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    
    writer.writerow({
        'question': "Question 1: Do you prefer A or B?",
        'answers': "A,B",
        'follow_ups': "question2,question3"
    })
    
    writer.writerow({
        'question': "Question 2: Why do you prefer A?",
        'answers': "Reason 1,Reason 2",
        'follow_ups': ","
    })
    
    writer.writerow({
        'question': "Question 3: Why do you prefer B?",
        'answers': "Reason 1,Reason 2",
        'follow_ups': ""
    })

# Read the decision tree from the CSV file
read_tree = build_decision_tree_from_csv('_decision_tree.csv')

# Now you can use the `run_decision_tree` function with the read_tree
answers = run_decision_tree(read_tree, read_tree['Question 1: Do you prefer A or B?'])

# Print the collected answers
print("\nAnswers:")
for i, answer in enumerate(answers):
    print(f"Question {i + 1}: {answer}")