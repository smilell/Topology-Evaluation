# Topology-Evaluation
Evaluate the Betti numbers and Euler characteristics for the segmentations.

## Overview

The `evaluation.py` script is designed for computing topological features of a given map using persistent homology. Specifically, it calculates the Betti numbers and the Euler characteristic of the map, which are fundamental metrics in topological data analysis.

## Requirements

- Python 3.x
- Numpy
- GUDHI library

Ensure you have the above prerequisites installed in your environment before running the script.

## Usage

To use this script, you need to have a map represented as a numpy array. The script processes this map to compute its Betti numbers and Euler characteristic.

1. Import the necessary function from the script:
   ```python
   from evaluation import compute_topological_features
   ```

2. Prepare your segmentation map as a numpy array.

3. Call the function with your map:
    ```python
    betti_numbers, euler_characteristic = compute_topological_features(your_map)
    ```
    `compute_topological_features()` : Takes a numpy array representing the map as input and returns a tuple containing the Betti numbers (0-dimensional, 1-dimensional, and 2-dimensional) and the Euler characteristic of the map.

### Acknowledegment
This project is developed based on the code originally developed by Priscille de Dumast. 
If you have any questions, please contact liu.li20@imperial.ac.uk
