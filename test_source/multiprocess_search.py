import os
import multiprocessing
import time

def search_keywords_in_file(file_path, keywords, queue):
    try:
        results = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    if keyword not in results:
                        results[keyword] = []
                    results[keyword].append(file_path)
        queue.put(results)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def multiprocess_search(files, keywords):
    processes = []
    queue = multiprocessing.Queue()
    results = {}
    
    for file_path in files:
        process = multiprocessing.Process(target=search_keywords_in_file, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    while not queue.empty():
        result = queue.get()
        for key in result:
            if key not in results:
                results[key] = []
            results[key].extend(result[key])
    
    return results

if __name__ == "__main__":
    files = [os.path.join('test_files', f) for f in os.listdir('test_files')]
    keywords = ['keyword1', 'keyword2', 'keyword3']
    
    start_time = time.time()
    results = multiprocess_search(files, keywords)
    end_time = time.time()
    
    print(f"Multiprocessing results: {results}")
    print(f"Time taken: {end_time - start_time} seconds")