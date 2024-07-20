import requests
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def fetch_text(url):
    response = requests.get(url)
    return response.text

def map_reduce(data, map_func, reduce_func):
    mapped_data = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(map_func, chunk): chunk for chunk in data}
        for future in as_completed(futures):
            mapped_data.extend(future.result())

    return reduce_func(mapped_data)

def map_words(text):
    words = text.split()
    return [(word.lower(), 1) for word in words]

def reduce_word_counts(mapped_data):
    counter = Counter()
    for word, count in mapped_data:
        counter[word] += count
    return counter

def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xticks(rotation=45)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Analyze word frequency from URL text')
    parser.add_argument('url', help='URL to fetch text from')
    parser.add_argument('--top_n', type=int, default=10, help='Number of top words to visualize')
    args = parser.parse_args()

    text = fetch_text(args.url)
    word_counts = map_reduce([text], map_words, reduce_word_counts)
    visualize_top_words(word_counts, args.top_n)

if __name__ == '__main__':
    main()