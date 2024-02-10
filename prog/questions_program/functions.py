import os
import csv 
from constants import csv_file, file_path, directory

def read_questions_and_answers():
    questions = []
    answers = []

    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        for row in reader:
            question = row[0]
            answer_list = row[1:]  # Answers are from the second column onwards
            questions.append(question)
            answers.append(answer_list)

    return questions, answers


def gather_questions_and_answers():
    questions = []  # Initialize an empty list to store the questions
    answers = []    # Initialize an empty list to store the answers

    while True:
        question = input("Enter a question (or type 'enough' to finish): ")
        
        if question.lower() == 'enough':
            break  # Exit the loop if the user types 'enough'
        
        questions.append(question)
        
        question_answers = []  # Initialize a list to store the answers for this question
        while True:
            answer = input("Enter an answer to that question (or type 'done' to finish): ")
            if answer.lower() == 'done':
                break  # Exit the inner loop if the user types 'done'
            question_answers.append(answer)
        
        answers.append(question_answers)  # Append the list of answers to the answers list

    # Save the data to a CSV file with horizontal answers
    # csv_file = "_questions_and_answers_horizontal.csv"
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Question"] + [f"Answer {i+1}" for i in range(len(questions))])  # Write header row
        for question, answer_list in zip(questions, answers):
            writer.writerow([question] + answer_list)  # Write the question and answers horizontally

    print(f"\nThe questions and answers have been saved to {csv_file} in directory {directory}.")



def create_dictionary():
    dictionary = {}
    while True:
        question = input("Enter a question (or type 'done' to finish): ")
        if question.lower() == 'done':
            break

        answers = {}
        while True:
            answer = input(f"Enter an answer for '{question}' (or type 'done' to finish): ")
            if answer.lower() == 'done':
                break
            action = input(f"Enter the action for answer '{answer}': ")
            answers[answer] = action

        dictionary[question] = answers

    return dictionary

def save_to_csv(dictionary, filename):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Question', 'Answer', 'Action'])
        for question, answers in dictionary.items():
            for answer, action in answers.items():
                writer.writerow([question, answer, action])

def create_dictionary_action(available_actions):
    dictionary = {}
    while True:
        question = input("Enter a question (or type 'done' to finish): ")
        if question.lower() == 'done':
            break

        answers = {}
        while True:
            answer = input(f"Enter an answer for '{question}' (or type 'done' to finish): ")
            if answer.lower() == 'done':
                break

            # Display the available actions for selection
            print("Available actions:")
            for i, action in enumerate(available_actions):
                print(f"{i + 1}. {action}")
            action_choice = int(input("Select the action (enter the corresponding number): "))

            # Ensure the selected action is within a valid range
            if 1 <= action_choice <= len(available_actions):
                action = available_actions[action_choice - 1]
                answers[answer] = action
            else:
                print("Invalid action choice. Please try again.")

        dictionary[question] = answers

    return dictionary

def run_decision_tree(tree, current_question):
    answer_list = []
    
    while True:
        # Print the current question
        print(current_question['question'])
        
        # Display available answers
        for i, answer in enumerate(current_question['answers']):
            print(f"{i + 1}. {answer}")
        
        # Get user input
        choice = input("Enter your choice (1, 2, etc.): ")
        
        try:
            choice = int(choice)
            if 1 <= choice <= len(current_question['answers']):
                answer_list.append(current_question['answers'][choice - 1])
                follow_up = current_question['follow_ups'][choice - 1]
                if follow_up is None:
                    break
                current_question = tree[follow_up]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return answer_list

def build_decision_tree_from_csv(csv_file):
    decision_tree = {}
    
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['question']
            answers = row['answers'].split(',')
            follow_ups = row['follow_ups'].split(',') if row['follow_ups'] else [None] * len(answers)
            
            decision_tree[question] = {
                'question': question,
                'answers': answers,
                'follow_ups': follow_ups
            }
    
    return decision_tree