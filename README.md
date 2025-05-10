# Emily: AI Sommelier Assistant

Emily is an intelligent sommelier assistant designed to provide personalized wine recommendations based on visual input (images of wine shelves) and user preferences. It leverages the OpenAI Assistants API, including Vision capabilities, Retrieval-Augmented Generation (RAG), and Function Calling. This project was developed for COMP47980: Generative AI and Language Models. Emily's persona is "Emy," a friendly, witty French sommelier.

## Project Goal

Emily aims to offer a specialized wine recommendation service superior to generic LLMs by:
1.  Analyzing images of wine shelves.
2.  Enriching wine data using a curated, localized knowledge base (`tescoRAG.json` for Irish supermarkets).
3.  Fetching external reviews/scores via web searches (Function Calling).
4.  Recommending the most suitable wine based on user preferences.

## Features

-   **Image-Based Wine Recognition:** Uses `gpt-4o` vision.
-   **Retrieval-Augmented Generation (RAG):** Consults `tescoRAG.json` for localized wine details.
-   **Function Calling:** Employs `duckduckgo-search` for external reviews/scores.
-   **User Preference Matching:** Considers budget, color, occasion, body, dryness, and flavor.
-   **Persona-Driven Output:** Recommendations by "Emy."

## How It Works (Workflow)

1.  **Input:** User provides an image URL of a wine shelf and preferences.
2.  **Vision (Chat Completions):** `gpt-4o` analyzes the image, outputting an initial JSON list of wines.
3.  **Assistant Run (Single Run):**
    -   The vision output, user preferences, and detailed instructions are sent to the "Emy" Assistant.
    -   **RAG:** Assistant uses File Search on `tescoRAG.json` (via a Vector Store) for enrichment.
    -   **Function Call:** If needed, calls `get_wine_reviews_from_web` Python function (using `duckduckgo-search`) for missing scores/notes. Snippets are returned.
    -   **Synthesis & Recommendation:** Assistant processes all data, analyzes against preferences, selects the best wine, and generates the final description.
4.  **Output:** Sommelier recommendation text is presented.

## Technologies Used

-   Python 3.x, Google Colaboratory
-   OpenAI Python Library (`openai` v1.x.x): Assistants API (Threads, Runs, Tools - File Search, Function), Chat Completions API (Vision), Files API, Vector Stores.
-   `duckduckgo-search`
-   JSON

## Setup and Installation (Colab)

### Prerequisites

-   OpenAI API key ( set up your own, i wont leak mine ;p)
-   `tescoRAG.json` file (curated wine data).

### Configuration

1.  **Open Notebook:** Upload/open the `.ipynb` file in Colab.
2.  **API Key:** Add your OpenAI API key to Colab Secrets as `API_KEY`.
3.  **RAG File:** Upload `tescoRAG.json` to your Colab session (e.g., `/content/`) or Google Drive, and ensure the script's filepath is correct.
4.  **Run Cells:** Execute notebook cells sequentially to install libraries, initialize the client, and run the assistant workflow. Update `img_linkX` for the image to be analyzed.

### Key Components

-   **Vision Input:** `gpt-4o` provides an initial JSON list of wines from an image.
-   **Assistant:** "Emy" persona, configured with `gpt-4o` (or `gpt-4o-mini`), File Search, and Function Calling tools. Instructions guide its multi-step reasoning.
-   **RAG Data (`tescoRAG.json`):** Curated/scraped Tesco Ireland wine data, uploaded to a Vector Store and linked to the Assistant for localized enrichment.
-   **Function Calling (`get_wine_reviews_from_web`):** Uses `duckduckgo-search` for targeted web queries on wine reviews/scores, returning snippets to the Assistant.
-   **User Preferences:** Dictionaries define categories (price, color, etc.) for user input, which are then formatted into the prompt for the Assistant.

**Example:**
-   **Input:** Image of various white wines, preference for "Cheap, White, Casual Chilling, Fruity."
-   **Process:** Emily identifies wines, uses RAG to add details (e.g., ABV for Viña Sol from catalog), then uses web search for a Vivino score for Viña Sol.
-   **Output (Emy):** "Bonjour! For your casual evening, the Viña Sol Sauvignon Blanc is a charming choice under €10! It's dry and fruity with lovely citrus notes, perfect for relaxing. Users on Vivino give it a solid 3.5/5. Santé!"

## Running the Web Scraper (`webscrape.py`) - Important Header Configuration

The `webscrape.py` script is designed to fetch wine data directly from Tesco Ireland's website. To make this script work, you **MUST** manually update it with fresh session headers from your own browser, as Tesco uses these for session management and security.

**These values are session-specific, will expire, and need to be updated each time you intend to run the scraper for an extended period or after some inactivity.**

**Steps to Obtain and Configure Headers:**

1.  **Open Tesco Website:** Navigate to the Tesco Ireland wine search results page in your web browser (e.g., Google Chrome or Firefox):
    `https://www.tesco.ie/groceries/en-IE/search?query=wine`

2.  **Open Developer Tools:**
    *   Press `F12` (or `Fn+F12` on some laptops).
    *   Alternatively, right-click anywhere on the page and select "Inspect" or "Inspect Element."

3.  **Go to the "Network" Tab:** In the Developer Tools panel, click on the "Network" tab.

4.  **Filter for "Fetch/XHR":** Within the Network tab, find the filter options and select "Fetch/XHR" to see only data requests.

5.  **Trigger the Data Request:**
    *   Reload the Tesco wine page (`Ctrl+R` or `Cmd+R`).
    *   Scroll down the page, or click to the next page of results (e.g., "Page 2"). This should trigger the relevant data request.

6.  **Find the `resources` POST Request:**
    *   Look through the list of Fetch/XHR requests. You are looking for a request whose **Name** is `resources` and whose **Method** is `POST`. It will likely be a request made to a URL similar to `https://www.tesco.ie/groceries/en-IE/resources`.
    *   Click on this specific `resources` request line to open its details.

7.  **Copy Request Headers:**
    *   In the details panel for the `resources` request, go to the **"Headers"** tab.
    *   Scroll down to the section labeled **"Request Headers"**.
    *   You need to copy the *values* for the following headers:
        *   `cookie`: This will be a very long string. Copy the entire value.
        *   `x-csrf-token`: Copy its value.
        *   *(Optional but recommended): Also note down values for `user-agent`, `accept`, `accept-language`, `origin`, `referer` if you want to be extremely precise, though the script includes common defaults for these.*

8.  **Update `webscrape.py`:**
    *   Open the `webscrape.py` file in a text editor.
    *   Locate the `request_headers` dictionary near the top of the script.
    *   **Carefully replace the placeholder values** for `'cookie'` and `'x-csrf-token'` with the values you just copied from your browser:

        ```python
        request_headers = {
            # ... other headers ...
            'cookie': 'YOUR_COPIED_COOKIE_STRING_GOES_HERE',
            'x-csrf-token': 'YOUR_COPIED_X_CSRF_TOKEN_GOES_HERE',
            # ... other headers ...
        }
        ```

9.  **Save and Run:** Save the `webscrape.py` file. You can now try running the script.

**Important Reminders:**

*   **Expiration:** These `cookie` and `x-csrf-token` values are temporary. If the scraper stops working (e.g., you get 403 Forbidden errors), the first thing to do is repeat steps 1-8 to get fresh header values.
*   **Responsibility:** Web scraping can be resource-intensive for websites. This script includes delays between page requests. Please use it responsibly and be mindful of Tesco's Terms of Service, which may prohibit automated scraping.
*   **Fragility:** Website structures can change, which may break this scraper. It may require updates if Tesco modifies its site.

By following these steps, you provide the scraper with the necessary session information to mimic a legitimate browser request, increasing the chances of a successful data fetch.


## Limitations

-   Vision accuracy can vary.
-   RAG data quality and staleness are critical.
-   Web search snippet quality limits external data richness.
-   LLM interpretation for summarization and complex single-run instruction following can be imperfect.
-   API rate limits may be encountered.

## Future Work

-   Expand and automate RAG dataset updates.
-   Refine to a two-run strategy (enrichment then recommendation) for potentially cleaner data handling.
-   Implement explicit Python-based filtering after enrichment.
-   Add more function calls (e.g., real-time stock APIs).
-   Develop a user-friendly interface (Streamlit/Gradio).


