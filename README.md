# Scribd Document Scraper

## About

A Python-based scraper for extracting document search results from Scribd using search queries and optional upload date filters.
The script collects document metadata such as title, author, views, page count, upload date, thumbnail, and document URL, then exports the results to a CSV file. This project allows you to search Scribd documents directly from the command line and export structured data into a CSV file for further analysis or archiving.

### Key Features

- Search Scribd documents by keyword
- Filter documents by upload date
- Export results to CSV
- Extract detailed metadata: Document title, Description, Author information, Views count, Upload date, Upvotes / Downvotes, Page count, Thumbnail URL, Document URL
- Automatic pagination
- Randomized delays to reduce rate limiting risk
- Browser impersonation using curl_cffi

### Prerequisites

- Python 3.11 or higher
- Required libraries:
    - `curl_cffi`
    - `pandas`

Install the dependencies using pip:

```bash
pip install curl_cffi pandas
```

### How to Use

Run the script from the command line using a search query.

```bash
python scraper.py --query <QUERY> [--date_limit <DATE_LIMIT>] [--document_limit <DOCUMENT_LIMIT>]
```


#### Arguments

| Argument           | Type      | Description                                   |
| ------------------ | --------- | --------------------------------------------- |
| `--query`          | `string`  | Search query used to find documents on Scribd |
| `--date_limit`     | `string`  | Filter results by upload date                 |
| `--document_limit` | `integer` | Maximum number of documents to scrape         |

##### Supported Date Filters

| Value    | Description                             |
| -------- | --------------------------------------- |
| `1week`  | Documents uploaded in the last week     |
| `1month` | Documents uploaded in the last month    |
| `3month` | Documents uploaded in the last 3 months |
| `6month` | Documents uploaded in the last 6 months |
| `1year`  | Documents uploaded in the last year     |



#### Example
```bash
python scraper.py \
  --query "machine learning" \
  --date_limit 1week \
  --document_limit 100
```

### Output

The scraped data is saved into a CSV file named `scribd_documents.csv` in the current directory.

| Column        | Description          |
| ------------- | -------------------- |
| `doc_id`      | Document ID          |
| `doc_type`    | Type of document     |
| `title`       | Document title       |
| `description` | Document description |
| `read_url`    | Scribd reader URL    |
| `thumbnail`   | Thumbnail image URL  |
| `author_name` | Author name          |
| `author_url`  | Author profile URL   |
| `views`       | Total views          |
| `page_count`  | Number of pages      |
| `upload_date` | Upload timestamp     |
| `upvotes`     | Upvote count         |
| `downvotes`   | Downvote count       |

### Notes

- Scribd may change its API or response structure at any time.
- Excessive requests may trigger temporary rate limiting.
- The script uses randomized sleep intervals between requests to reduce detection risk.