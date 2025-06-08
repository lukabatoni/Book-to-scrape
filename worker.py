import json
from multiprocessing import Queue
from utils import make_request, save_data

def scrape_book_page(url):
    soup = make_request(url)
    book = {
        'title': soup.find('h1').text,
        'price': soup.find('p', class_='price_color').text,
        'stock': soup.find('p', class_='instock').text.strip(),
        'description': soup.find('div', id='product_description').find_next_sibling('p').text if soup.find('div', id='product_description') else None
    }
    return book

def worker(task_queue: Queue, result_queue: Queue):
    while True:
        task = task_queue.get()
        if task == 'STOP':
            break
        
        try:
            if task['type'] == 'category':
                # Scrape all books in a category
                soup = make_request(task['url'])
                books = []
                for book in soup.find_all('article', class_='product_pod'):
                    book_url = book.find('h3').find('a')['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
                    books.append(scrape_book_page(book_url))
                
                filename = f"category_{task['name']}.json"
                save_data(books, filename)
                result_queue.put({'task': task, 'status': 'success', 'filename': filename})
                
            elif task['type'] == 'book':
                # Scrape a single book
                book = scrape_book_page(task['url'])
                filename = f"book_{task['name']}.json"
                save_data(book, filename)
                result_queue.put({'task': task, 'status': 'success', 'filename': filename})
                
        except Exception as e:
            result_queue.put({'task': task, 'status': 'failed', 'error': str(e)})