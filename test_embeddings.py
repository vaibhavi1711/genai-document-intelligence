import numpy as np

emb = np.load("data/embeddings.npy")

print("Number of embeddings:", emb.shape[0])
print("Dimension of each embedding:", emb.shape[1])