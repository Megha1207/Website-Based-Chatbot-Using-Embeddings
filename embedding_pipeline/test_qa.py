from src.qa_engine import QAEngine

qa = QAEngine()

while True:
    q = input("\nAsk a question (or type 'exit'): ")
    if q.lower() == "exit":
        break

    print("\nAnswer:", qa.answer(q))
