import requests
import json
import time
import random

# --- (fetch_tesco_wine_page function remains the same, including the DEBUG print) ---
def fetch_tesco_wine_page(page_number, session_headers):
    """Fetches a specific page of wine results from Tesco resources endpoint."""
    print(f"\nAttempting to fetch page {page_number}...")
    url = "https://www.tesco.ie/groceries/en-IE/resources"
    payload = {
         "requiresAuthentication": False,
         "resources": [
             {
                 "type": "search",
                 "params": {
                     "query": {
                         "query": "wine",
                         "icid": "tescohp_sws-1_m-ft_in-wine_out-wine",
                         "department": "Wine",
                         "viewAll": "department",
                         "page": str(page_number)
                     }
                 },
                 "hash": "8924798660881233"
             }
         ],
         "sharedParams": {
              "query": {
                  "query": "wine",
                  "icid": "tescohp_sws-1_m-ft_in-wine_out-wine",
                  "department": "Wine",
                  "viewAll": "department",
                  "page": str(page_number)
              }
         }
    }
    try:
        response = requests.post(url, headers=session_headers, json=payload, timeout=30)
        response.raise_for_status()
        print(f"Request for page {page_number} successful! Status Code: {response.status_code}")
        try:
            data = response.json()
            # ---- Keep the debug print for now ----
            print(f"\n--- RAW JSON Response for Page {page_number} ---")
            # print(json.dumps(data, indent=2)) # Can comment out if too long, but keep for first run
            print("--- (Raw JSON Printing) ---")
            # ---- End Debug Print ----
            return data
        except json.JSONDecodeError:
             print("Error: Failed to decode JSON response from server (DEBUG).")
             print(f"Raw response text: {response.text[:1000]}...")
             return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error fetching page {page_number}: {e.response.status_code} {e.response.reason}")
        if e.response.status_code == 403: print("Received 403 Forbidden - Check Headers.")
        elif e.response.status_code == 429: print("Received 429 Too Many Requests - Increase delays.")
        print(f"Response Body: {e.response.text[:500]}...")
        return None
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching page {page_number}.")
        return None
    except requests.exceptions.RequestException as e:
         print(f"Network Error during requests call for page {page_number}: {e}")
         return None
    except Exception as e:
        print(f"An unexpected error occurred fetching page {page_number}: {e}")
        return None

# --- Main Script Logic ---
request_headers = {
    # --- PASTE YOUR CURRENT HEADERS HERE ---
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'cookie': 'YOUR_COOKIE_STRING_HERE_FROM_BROWSER_DEVTOOLS',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM1MTI5NTQiLCJhcCI6IjExMzQyNDYxMjUiLCJpZCI6ImE3MDFmNTBhZjMzZWUxYWMiLCJ0ciI6Ijc5OWVkMmNiMTliODcwOTBjMzM2ZmE3MjA5ZGY4ZjdjIiwidGkiOjE3NDU1MzE3ODU1MTAsInRrIjoiMzI5NjIzNSJ9fQ==',
    'origin': 'https://www.tesco.ie',
    'priority': 'u=1, i',
    'referer': 'https://www.tesco.ie/groceries/en-IE/search?query=wine&icid=tescohp_sws-1_m-ft_in-wine_out-wine&department=Wine&viewAll=department&page=1',
    'sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-799ed2cb19b87090c336fa7209df8f7c-a701f50af33ee1ac-01',
    'tracestate': '3296235@nr=0-1-3512954-1134246125-a701f50af33ee1ac----1745531785510',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'x-csrf-token': 'YOUR_X_CSRF_TOKEN_HERE_FROM_BROWSER_DEVTOOLS',
    'x-queueit-ajaxpageurl': 'false',
    'x-requested-with': 'XMLHttpRequest'
}

# --- Variables for looping ---
start_page = 1
max_pages_to_fetch = 20 # Limit how many pages to fetch
all_wine_products = [] # List to store raw results from all pages
total_pages_available = 1 # Initialize

# --- Loop through pages ---
print("Starting Tesco wine scrape...")
for current_page_number in range(start_page, max_pages_to_fetch + 1):

    # Check if we need to fetch this page
    if current_page_number > total_pages_available and total_pages_available != 1:
         print(f"\nReached calculated end of results ({total_pages_available} pages). Stopping.")
         break

    # Fetch data for the current page
    page_data = fetch_tesco_wine_page(current_page_number, request_headers)

    # Process the data if the fetch was successful
    if page_data:
        try:
            # --- CORRECTED EXTRACTION LOGIC ---
            search_results = page_data.get('search') # Get the top-level 'search' object
            if search_results and isinstance(search_results, dict):
                results_data = search_results.get('data', {}).get('results', {}) # Navigate down
                product_items_on_page = results_data.get('productItems', [])
                page_info = results_data.get('pageInformation', {})
            else:
                 # Handle case where 'search' key is missing or not a dict
                 product_items_on_page = []
                 page_info = {}
                 print(f"Warning: 'search' key missing or invalid in response for page {current_page_number}.")
            # --- END CORRECTION ---

            total_count = page_info.get('totalCount', 0)
            page_size = page_info.get('pageSize', 24)
            if page_size and page_size > 0:
                 total_pages_available = (total_count + page_size - 1) // page_size
            else:
                 total_pages_available = current_page_number # Assume last page if size invalid

            print(f"Page {current_page_number}/{total_pages_available}: Found {len(product_items_on_page)} items.")

            # Add the extracted items to our main list
            if product_items_on_page:
                all_wine_products.extend(product_items_on_page)
            else:
                # Check if this was expected (i.e., page > total_pages) or an error
                if current_page_number <= total_pages_available :
                    print(f"No product items found on page {current_page_number}, stopping.")
                else:
                     print(f"Reached end of results.")
                break # Stop if a page returns no items

            # Check if this was the last page based on calculation
            if current_page_number >= total_pages_available:
                 print(f"\nFetched the last available page ({total_pages_available}).")
                 break

        except (KeyError, TypeError, IndexError, AttributeError) as e:
            print(f"Error processing response structure for page {current_page_number}: {e}")
            # print(json.dumps(page_data, indent=2)) # Uncomment for debugging structure
            break # Stop on error

    else:
        # Fetch failed for this page (error already printed in function)
        print(f"Stopping scrape due to fetch error on page {current_page_number}.")
        break # Stop the loop if a page fetch fails

    # --- DELAY ---
    # Only sleep if we are not on the last page we intend to fetch OR the last available page
    if current_page_number < total_pages_available and current_page_number < (start_page + max_pages_to_fetch): # Adjusted loop end condition
        delay = random.uniform(4, 8) # Random delay between 4 and 8 seconds
        print(f"Waiting {delay:.2f} seconds before fetching page {current_page_number + 1}...")
        time.sleep(delay)

# --- End of Loop ---

print(f"\n------------------------------------------")
print(f"Scraping finished. Total wines collected: {len(all_wine_products)}")
# Use 'current_page_number' as it holds the last page *attempted* or *completed*
print(f"Fetched pages {start_page} through {current_page_number}.")
print(f"------------------------------------------")

# Now 'all_wine_products' list contains raw product data from the fetched pages
# Format this data as needed for your RAG file or further processing

final_wine_list = []
print("\nFormatting scraped data...")
for item in all_wine_products:
     try:
         product_info = item.get('product', {})
         if not product_info: continue

         title = product_info.get('title', 'N/A')
         wine_name = title
         unit_measure = product_info.get('unitOfMeasure')
         if unit_measure and title.endswith(unit_measure):
              wine_name = title[:-len(unit_measure)].strip()

         region = product_info.get('shelfName', None)

         wine_entry = {
             "producer_brand": product_info.get('brandName', None),
             "wine_name": wine_name if wine_name != title else product_info.get('title', None),
             "region": region,
             "price_eur": product_info.get('price', None),
             "tesco_id": product_info.get('id', None),
             "image_url": product_info.get('defaultImageUrl', None),
             "size": unit_measure,
             "promotions": item.get('promotions', [])
         }
         if wine_entry["producer_brand"] or wine_entry["wine_name"]:
              final_wine_list.append(wine_entry)

     except Exception as e:
          print(f"Error formatting item: {e} - Item: {item}")

print(f"Formatted {len(final_wine_list)} wine entries.")

# Optional: Print the formatted list snippet
print("\n--- Formatted List Snippet (First 5) ---")
print(json.dumps(final_wine_list[:5], indent=2))

# Optional: Save the full list to a JSON file
try:
    with open("tesco_wines_scraped.json", "w", encoding='utf-8') as f:
        json.dump(final_wine_list, f, indent=2, ensure_ascii=False)
    print("\nSaved formatted list to tesco_wines_scraped.json")
except Exception as e:
    print(f"\nError saving formatted list to file: {e}")