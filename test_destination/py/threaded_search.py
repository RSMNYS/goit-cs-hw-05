import os
import threading
import time

def search_keywords_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    if keyword not in results:
                        results[keyword] = []
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def threaded_search(files, keywords):
    threads = []
    results = {}
    for file_path in files:
        thread = threading.Thread(target=search_keywords_in_file, args=(file_path, keywords, results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return results

if __name__ == "__main__":
    files = [os.path.join('test_files', f) for f in os.listdir('test_files')]
    keywords = ['keyword1', 'keyword2', 'keyword3'] 
    
    start_time = time.time()
    results = threaded_search(files, keywords)
    end_time = time.time()
    
    print(f"Threading results: {results}")
    print(f"Time taken: {end_time - start_time} seconds")