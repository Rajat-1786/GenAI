import json
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from chunking import chunk
import voyageai
import chromadb 
from voyage_ai_embed import voyage_ai
from dotenv import load_dotenv

load_dotenv()

def main():
    project_dir = Path(__file__).resolve().parents[2]
    search_dir = Path(__file__).resolve().parent
    voyage_client = voyage_ai(voyageai.Client())
    chroma_collections = chromadb.PersistentClient(path=str(project_dir / "chroma_db")).get_or_create_collection(
    name="docs",
    metadata={"hnsw:space": "cosine"},                    # cosine distance
)

    corpus_dir = project_dir / "corpus"
    files = sorted(corpus_dir.glob("*.pdf"))
    if not files:
        raise FileNotFoundError(f"No PDF files found in {corpus_dir}")

    chunk_obj = chunk(voyage_client,chroma_collections)
    for file in files:
        print(f"processing file: {file}")
        chunk_obj.save_embed_to_db(str(file))
        time.sleep(22)
        print(f"Process completted")
    
    with open(search_dir / "questions.json", "r") as f:
        dataset = json.load(f)

    dict_res = []
    for item in dataset:
        queries = item["query"]
        if not isinstance(queries, list) or not queries:
            raise ValueError(f"Expected a non-empty query list for source {item['source']}")

        for question_number, query in enumerate(queries, start=1):
            if not isinstance(query, str) or not query.strip():
                raise ValueError(f"Invalid question {question_number} for source {item['source']}")

            print(f"Processing question {question_number}/{len(queries)}: {query}")
            results = chunk_obj.find_most_similar_chunk(query)
            actual_source = results["metadatas"][0][0]["source"]
            source_match = actual_source == item["source"]
            dict_res.append({
                "query": query,
                "question_number": question_number,
                "valid": int(source_match),
                "source": int(source_match),
                "actual_source": actual_source,
                "expected_source": item["source"],
            })
            print("Process the query completed")
            time.sleep(22)

    with open(search_dir / "eval_results.json", "w") as f:
        json.dump(dict_res, f, indent=2)

if __name__ == "__main__":
    main()