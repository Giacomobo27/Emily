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

## Key Components

-   **Vision Input:** `gpt-4o` provides an initial JSON list of wines from an image.
-   **Assistant:** "Emy" persona, configured with `gpt-4o` (or `gpt-4o-mini`), File Search, and Function Calling tools. Instructions guide its multi-step reasoning.
-   **RAG Data (`tescoRAG.json`):** Curated/scraped Tesco Ireland wine data, uploaded to a Vector Store and linked to the Assistant for localized enrichment.
-   **Function Calling (`get_wine_reviews_from_web`):** Uses `duckduckgo-search` for targeted web queries on wine reviews/scores, returning snippets to the Assistant.
-   **User Preferences:** Dictionaries define categories (price, color, etc.) for user input, which are then formatted into the prompt for the Assistant.


**Example:**
-   **Input:** Image of various white wines, preference for "Cheap, White, Casual Chilling, Fruity."
-   **Process:** Emily identifies wines, uses RAG to add details (e.g., ABV for Viña Sol from catalog), then uses web search for a Vivino score for Viña Sol.
-   **Output (Emy):** "Bonjour! For your casual evening, the Viña Sol Sauvignon Blanc is a charming choice under €10! It's dry and fruity with lovely citrus notes, perfect for relaxing. Users on Vivino give it a solid 3.5/5. Santé!"

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


