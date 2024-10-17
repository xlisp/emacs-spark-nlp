import os
import re
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import faiss
from sklearn.decomposition import PCA
import sys
from utils.file_list import find_files_with_chinese_names
from utils.md_todos import get_todo_items
from utils.git_log import get_git_log

def get_embedding(text):
    response = requests.post('http://localhost:11434/api/embeddings', json={
        'model': 'nomic-embed-text',
        'prompt': text
    })
    return response.json()['embedding']

def save_embeddings_to_faiss(embeddings, db_path):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)  # L2 distance index
    index.add(np.array(embeddings).astype(np.float32))  # Add embeddings to the FAISS index
    faiss.write_index(index, db_path)

def load_embeddings_from_faiss(db_path):
    index = faiss.read_index(db_path)
    return index

def get_or_calculate_embeddings(todo_items, db_path):
    if os.path.exists(db_path):
        print("Loading embeddings from FAISS index...")
        index = load_embeddings_from_faiss(db_path)

        num_embeddings = index.ntotal
        dim = index.d

        embeddings = np.zeros((num_embeddings, dim))

        for i in range(num_embeddings):
            embeddings[i] = index.reconstruct(i)

        return embeddings
    else:
        print("Calculating new embeddings...")
        embeddings = []
        for _, todo in todo_items:
            print(f"Calculating embedding for: {todo}")
            embedding = get_embedding(todo)
            embeddings.append(embedding)

        save_embeddings_to_faiss(embeddings, db_path)
        return np.array(embeddings)

def group_todos(todo_items, embeddings, n_clusters=18):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    groups = {}
    for (filename, todo), label in zip(todo_items, labels):
        if label not in groups:
            groups[label] = []
        groups[label].append((filename, todo))

    return groups, labels, kmeans.cluster_centers_

def visualize_clusters_3d(embeddings, labels, cluster_centers, todo_items):
    embeddings = np.array(embeddings)

    combined = np.vstack((embeddings, cluster_centers))

    pca = PCA(n_components=3)
    combined_3d = pca.fit_transform(combined)

    embeddings_3d = combined_3d[:len(embeddings)]
    centers_3d = combined_3d[len(embeddings):]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(embeddings_3d[:, 0], embeddings_3d[:, 1], embeddings_3d[:, 2],
                         c=labels, cmap='viridis', alpha=0.7)

    ax.scatter(centers_3d[:, 0], centers_3d[:, 1], centers_3d[:, 2],
               c='red', marker='x', s=200, linewidths=3)

    for i, (filename, todo) in enumerate(todo_items):
        ax.text(embeddings_3d[i, 0] + 1, embeddings_3d[i, 1] + 1, embeddings_3d[i, 2] + 1,
                "", fontsize=8, alpha=0.7)

    plt.colorbar(scatter)

    ax.set_title('3D K-means Clustering of TODO Items (PCA)')
    ax.set_xlabel('PCA component 1')
    ax.set_ylabel('PCA component 2')
    ax.set_zlabel('PCA component 3')

    plt.tight_layout()
    plt.show()

def main():

    if len(sys.argv) != 4:
        print("Usage: python script.py <function_name> <index_file_name> <n_clusters>")
        sys.exit(1)

    function_name = sys.argv[1]
    index_file_name = sys.argv[2]
    n_clusters = int(sys.argv[3])

    if function_name == "find_files_with_chinese_names":
        todo_items = find_files_with_chinese_names()
    elif function_name == "get_todo_items":
        todo_items = get_todo_items()
    elif function_name == "get_git_log":
        todo_items = get_git_log()
    else:
        print(f"Unknown function: {function_name}")
        sys.exit(1)

    embeddings = get_or_calculate_embeddings(todo_items, index_file_name)

    #n_clusters = min(18, len(todo_items))

    groups, labels, cluster_centers = group_todos(todo_items, embeddings, n_clusters)

    for i, group in enumerate(groups.values()):
        print(f"Group {i+1}:")
        for filename, todo in group:
            print(f"  [{filename}] {todo}")
        print()

    visualize_clusters_3d(embeddings, labels, cluster_centers, todo_items)

if __name__ == "__main__":
    main()
