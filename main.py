import json
import time
from multiprocessing import Process, Queue
from utils import load_config, make_request
from worker import worker

def get_categories(base_url):
    soup = make_request(base_url)
    categories = []
    for category in soup.find('ul', class_='nav-list').find('ul').find_all('a'):
        categories.append({
            'name': category.text.strip(),
            'url': base_url + category['href']
        })
    return categories

def master():
    config = load_config()
    task_queue = Queue()
    result_queue = Queue()
    
    # Start worker processes
    workers = []
    for i in range(config['num_workers']):
        p = Process(target=worker, args=(task_queue, result_queue))
        p.start()
        workers.append(p)
        print(f"Started worker {i+1}")
    
    # Get categories and create tasks
    categories = get_categories(config['base_url'])
    for category in categories[:5]:  # Just do first 5 categories for demo
        task_queue.put({
            'type': 'category',
            'name': category['name'],
            'url': category['url']
        })
    
    # Monitor progress
    tasks_completed = 0
    tasks_failed = 0
    while tasks_completed + tasks_failed < 5:  # We submitted 5 tasks
        result = result_queue.get()
        if result['status'] == 'success':
            tasks_completed += 1
            print(f"Task completed: {result['task']['name']} (saved to {result['filename']})")
        else:
            tasks_failed += 1
            print(f"Task failed: {result['task']['name']} - {result['error']}")
    
    # Stop workers
    for _ in range(config['num_workers']):
        task_queue.put('STOP')
    
    for p in workers:
        p.join()
    
    print(f"\nScraping complete! Success: {tasks_completed}, Failed: {tasks_failed}")

if __name__ == '__main__':
    master()