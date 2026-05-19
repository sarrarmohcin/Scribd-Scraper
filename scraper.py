
from curl_cffi import requests
import argparse
import json
import time
import random
import pandas as pd


def get_documents(session, params, page):
    
    if page > 1:
        params['page'] = page

    try:
        response = session.get('https://www.scribd.com/search/query', params=params)
        response.raise_for_status()
        
        data = json.loads(response.content)
        documents = data['results']['documents']['content']['documents']
        
        results = []
        for doc in documents:
            # get title
            title = doc.get('title', None)
            if not title:
                continue
            
            # get document url
            read_url  = doc.get('reader_url', None)
            if not read_url:
                continue
            
            # get author
            author = None
            authors = doc.get('authors', [])
            if not authors:
                continue
            
            author = authors[0]
            author_name = author['name'] if 'name' in author else None
            author_url = author['url'] if 'url' in author else None
            if not author_name or not author_url:
                continue
            
            # get content
            description = doc.get('description', None)
            
            # get view count
            views = doc.get('views', None)
            
            # get upload date
            upload_date = doc.get('releasedAt', None)
            
            # get upvotes
            upvotes = doc.get('upvoteCount', None)
            
            # get downvotes
            downvotes = doc.get('downvoteCount', None)
            
            # get document type
            doc_type = doc.get('type', None)
            
            # get document id
            doc_id = doc.get('id', None)
            
            # get document page count
            page_count = doc.get('pageCount', None)
            
            # get language
            language = doc.get('language', {})
            if language and 'name' in language:
                lang = language['name']
            else:
                lang = None
                
            # get isUnlocked
            isUnlocked = doc.get('isUnlocked', None)
            


            
            # get media
            thumbnail = doc.get('retina_image_url', None)
            if not thumbnail:
                thumbnail = doc.get('image_url', None)
                
            
            results.append({
                'doc_id': doc_id,
                'doc_type': doc_type,
                'title': title,
                'description': description,
                'read_url': read_url,
                'thumbnail': thumbnail,
                'language': lang,
                'author_name': author_name,
                'author_url': f"https://www.scribd.com{author_url}" if author_url else None,
                
                'views': views,
                'page_count': page_count,
                'upload_date': upload_date,
                'upvotes': upvotes,
                'downvotes': downvotes,
                'isUnlocked': isUnlocked
            })
            
        
        return results
    except Exception as e:
        print(f"Error fetching documents: {e}")
        return []
    
    
    
  
if __name__ == "__main__":
    # Define arguments
    
    parser = argparse.ArgumentParser(description="Scrape documents from Scribd based on a search query.")
    parser.add_argument("--query", type=str, help="The search query to use for scraping.")
    parser.add_argument("--date_limit", type=str, help="The date limit for filtering results ('1week', '1month','3month','6month','1year).", default=None)
    parser.add_argument("--document_limit", type=int, help="The maximum number of documents to scrape.", default=100)
    
    args = parser.parse_args()
    
    # validate date limit
    if args.date_limit and args.date_limit not in ['1week', '1month', '3month', '6month', '1year']:
        print("Invalid date limit. Please choose from '1week', '1month', '3month', '6month', '1year'.")
        exit(1)
    
    # validate query
    if not args.query:
        print("Query is required.")
        exit(1)
        
    # validate document limit if integer
    if not isinstance(args.document_limit, int):
        print("Document limit must be an integer.")
        exit(1)
        
    # validate document limit
    if args.document_limit <= 0:
        print("Document limit must be a positive integer.")
        exit(1)
    
    

    args = parser.parse_args()
    
    params = {
        'query': args.query,
        'verbatim': 'true',
        'ct_lang': '0',
    }
    
    if args.date_limit:
        params['filters'] = json.dumps({'date_uploaded': args.date_limit})

    # create session
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://www.scribd.com/search',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    session = requests.Session()
    session.impersonate = "chrome120"
    session.headers.update(headers)
    
    page = 1
    data = []
    while True:
        documents = get_documents(session, params, page)
        if not documents:
            break
        data.extend(documents)
        if len(data) >= args.document_limit:
            break
        page += 1
        time.sleep(random.uniform(1, 3))  # Sleep to avoid rate limiting
        
    data = data[:args.document_limit]  # Limit to the specified number of documents
    
    # Save results to a CSV file
    df = pd.DataFrame(data)
    df.to_csv('scribd_documents.csv', index=False)
    print(f"Scraped {len(data)} documents. Results saved to 'scribd_documents.csv'.")