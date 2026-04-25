import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
print("All dependencies loaded successfully!")

# Quick test
arr = np.array([1, 2, 3])
print(f"Test array: {arr}")
print(f"Mean: {arr.mean()}")