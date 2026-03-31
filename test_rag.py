from rag.generator import generate_answer

question = "What is prompt engineering?"

answer, sources = generate_answer(question)

print("\n" + "="*50)

print("QUESTION:")
print(question)

print("\nANSWER:")
print(answer)

print("\nSOURCES:")
for s in sources:
    print(f"- {s}")

print("="*50)