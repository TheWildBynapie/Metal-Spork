import sys
import pandas as pd
import Bio
import numpy as np
import matplotlib
import sklearn
import scipy

print(f"Python Version: {sys.version.split()[0]}")
print(f"--- Standard Library Modules (argparse, re, pathlib, csv) ---")
print("Shared with Python interpreter version above.")
print("\n--- Third-Party Packages ---")
print(f"pandas: {pd.__version__}")
print(f"Biopython (Bio): {Bio.__version__}")
print(f"numpy: {np.__version__}")
print(f"matplotlib: {matplotlib.__version__}")
print(f"scikit-learn (sklearn): {sklearn.__version__}")
print(f"scipy: {scipy.__version__}")