from processor import load_document
from vector_store import build_vector_db, save_vector_db
import os


def store_policies():
    policy_folder = r"D:\Prescription_validation\Policies"
    db_path = r"D:\Prescription_validation\policy_db"

    policy_docs = []

    for file_name in os.listdir(policy_folder):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(policy_folder, file_name)
            print(f"📄 Loading policy: {file_name}")
            doc = load_document(file_path)
            policy_docs.append(doc)

    if not policy_docs:
        print("❌ No policy PDFs found.")
        return

    vector_db = build_vector_db(policy_docs)
    save_vector_db(vector_db, db_path)

    print(f"\n✅ Policy vector DB saved at: {db_path}")


if __name__ == "__main__":
    store_policies()