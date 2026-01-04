import sys
# Import the crawler module we created in Step 2
import crawler
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# [Fix] Force standard output to use UTF-8 explicitly
sys.stdout.reconfigure(encoding='utf-8')

def create_vector_db():
    """
    1. Collects news using the crawler.
    2. Converts text to vectors using a HuggingFace model.
    3. Saves the vectors to a local ChromaDB.
    """
    
    # 1. Get data from Hacker News
    print(">>> [1/4] Scraping Hacker News...")
    news_list = crawler.get_tech_news()
    
    if not news_list:
        print("No news found. Check your internet connection or crawler.")
        return None

    # 2. Convert to LangChain Document format
    # The 'Document' object is what LangChain uses to handle text
    documents = []
    for news in news_list:
        # We combine title and link so the AI can read both
        page_content = f"Title: {news['title']}\nLink: {news['link']}"
        
        # Metadata is useful for filtering later (optional)
        metadata = {"source": news['link'], "title": news['title']}
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)
    
    print(f">>> [2/4] Prepare {len(documents)} documents.")

    # 3. Initialize Embedding Model (Runs Locally)
    # "all-MiniLM-L6-v2" is a fast and efficient model for sentence embeddings
    print(">>> [3/4] Loading Embedding Model (This might take a moment)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Create and Save Vector Store (ChromaDB)
    # The database will be saved in a folder named './chroma_db'
    print(">>> [4/4] Creating Vector Database...")
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db" # Save to disk
    )
    
    print("✅ Success! Database saved to './chroma_db'")
    return db

def test_search(query):
    """
    Tests if the vector search is working correctly.
    """
    print(f"\n🔍 Testing Search Query: '{query}'")
    
    # Load the DB from disk
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # Search for the most similar documents (k=3 means top 3 results)
    results = db.similarity_search(query, k=3)
    
    for i, doc in enumerate(results):
        print(f"\n[Result {i+1}]")
        print(doc.page_content)

if __name__ == "__main__":
    # 1. Create the DB (Run this once to save data)
    create_vector_db()
    
    # 2. Test the DB (Ask a question related to tech)
    # You can change the query to test different topics
    test_search("google or ai")