import numpy as np

class Aggregator:

    def _get_weights(self, embeddings: np.array):
        n = embeddings.shape[0]
        positions = np.arange(1, n + 1)
        weights = 1 / positions

        return weights

    def get_average_embedding(self, embeddings: np.array, weights: np.array = None):
        if not weights:
            weights = self._get_weights(embeddings)

        average_embedding = np.average(embeddings, axis=0, weights=weights)

        return average_embedding