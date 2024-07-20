import os
from faker import Faker
import random

fake = Faker()

def create_test_file(filename, num_words, keywords):
    with open(filename, 'w', encoding='utf-8') as f:
        words = [fake.word() for _ in range(num_words)]
        for _ in range(len(words) // 10):  # Insert keywords at random positions
            words[random.randint(0, len(words) - 1)] = random.choice(keywords)
        f.write(' '.join(words))

def generate_test_files(num_files, num_words_per_file, keywords):
    os.makedirs('test_files', exist_ok=True)
    for i in range(num_files):
        create_test_file(f'test_files/file{i + 1}.txt', num_words_per_file, keywords)

if __name__ == "__main__":
    keywords = ['keyword1', 'keyword2', 'keyword3']
    generate_test_files(10, 1000, keywords)  # Generates 10 files, each with 1000 words
    print("Test files generated in the 'test_files' directory.")