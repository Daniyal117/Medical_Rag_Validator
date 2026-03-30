from processor import load_document
from vector_store import load_vector_db
from extractor import extract_prescription_data
from validator import validate


def run():
    db_path = r"D:\Prescription_validation\policy_db"

    vector_db = load_vector_db(db_path)
    print("✅ Policy vector DB loaded")

    pres_doc = load_document(r"D:\Prescription_validation\Prescription\Q125_Notes.pdf")

    pres_json = extract_prescription_data(pres_doc.page_content)
    print("\n📄 Extracted prescription JSON:\n")
    print(pres_json)

    policy_chunks = vector_db.similarity_search(pres_json, k=5)

    print("\n📚 Retrieved policy chunks:\n")
    for i, chunk in enumerate(policy_chunks, 1):
        print(f"\n--- Chunk {i} ---\n")
        print(chunk.page_content[:700])

    result = validate(pres_json, policy_chunks)

    print("\n✅ FINAL VALIDATION RESULT:\n")
    print(result)


if __name__ == "__main__":
    run()