import csv
from constants import csv_file, file_path
from functions import read_questions_and_answers
import os 

def main():
    questions, answers = read_questions_and_answers()

    answered_questions = []

    for i, (question, answer_list) in enumerate(zip(questions, answers), start=1):
        print(f"{i}. Question: {question}")
        for j, answer in enumerate(answer_list, start=1):
            print(f"   Answer {j}: {answer}")

        user_response = input("Press Enter if answered, or type 'skip' to move to the next question: ")

        if user_response.lower() != "skip":
            answered_questions.append((question, answer_list))

        print("\nAnswered Questions:")
        for answered_question, answered_answers in answered_questions:
            print(f"Question: {answered_question}")
            for j, answered_answer in enumerate(answered_answers, start=1):
                print(f"   Answer {j}: {answered_answer}")
        print()

    print("All questions have been presented.")

    if answered_questions:
        print("Your answers:")
        for answered_question, answered_answers in answered_questions:
            print(f"Question: {answered_question}")
            for j, answered_answer in enumerate(answered_answers, start=1):
                print(f"   Your Answer {j}: {answered_answer}")

if __name__ == "__main__":
    main()
