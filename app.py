from rag.generator import generate_answer

print("GenAI Document Intelligence")
print("Type 'exit' to quit\n")

while True:
    
    question = input("\nAsk a question: ")
    
    if question.lower() == "exit":
        break
    
    answer, sources = generate_answer(question)
    
    print("\nANSWER:")
    print(answer)
    
    print("\nSOURCES:")
    for s in sources:
        print(f"- {s}")