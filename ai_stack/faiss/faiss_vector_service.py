
import os
import json
import numpy as np
import faiss


class FAISSVectorService:

    def __init__(self, dimension=384):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.metadata = []

    def add_vectors(
        self,
        vectors,
        metadata
    ):

        vectors = np.asarray(
            vectors,
            dtype="float32"
        )

        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected dimension {self.dimension}, "
                f"got {vectors.shape[1]}"
            )

        self.index.add(vectors)
        self.metadata.extend(metadata)

        return {
            "status": "success",
            "vectors_added": len(vectors),
            "total_vectors": self.index.ntotal
        }

    def search(
        self,
        query_vector,
        top_k=5
    ):

        query_vector = np.asarray(
            query_vector,
            dtype="float32"
        )

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        distances, indices = self.index.search(
            query_vector,
            min(top_k, self.index.ntotal)
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index < 0:
                continue

            results.append({
                "distance": float(distance),
                "metadata": self.metadata[index]
            })

        return {
            "status": "success",
            "results": results
        }

    def count(self):

        return self.index.ntotal
