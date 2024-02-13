import json
import numpy as np
import time

class GetTopSimilar():
    def __init__(self, input_array, compare_matrix):
        distances = np.linalg.norm(compare_matrix - input_array, axis=1)
        self.recycled_id = np.argsort(distances)
        self.euclidean_distances = distances[self.recycled_id]



# if __name__ == "__main__":
#     input_array = np.array([0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#     with open('data.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     compare_matrix = np.array(data["annotation"][0]["annotation_matrix"])

#     print(GetTopSimilar(input_array, compare_matrix).euclidean_distances)

        


