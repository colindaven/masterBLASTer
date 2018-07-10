import sys
import os
import pandas as pd
import numpy as np

# Extract command line output filename
outfile = sys.argv[1]

bestBLASTHitsOnly=True

def count_hits(row, hit_table):
    count = sum(protein_list == row['name'])
    return count

filelist=os.listdir("temp/")

protein_list = np.array([],dtype = 'str') 

# Parse blast files if not empty and combine the results into a single vector
for file in filelist:
    if file.startswith('blastout'):
        if os.path.getsize(file) > 0:
            if (bestBLASTHitsOnly):
                temp_table = pd.read_table(f"temp/{file}", delimiter = '\t', header = None, nrows = 1, usecols = [2])
            else:
                temp_table = pd.read_table(f"temp/{file}", delimiter = '\t', header = None, usecols = [2])
            protein_list = np.append(protein_list, temp_table.iloc[:,0].ravel())

unique_counts = np.unique(protein_list, return_counts=True)
results_table = pd.DataFrame({'name':unique_counts[0], 'count':unique_counts[1]})
results_table = results_table.sort_values(by = 'count', ascending = False)
results_table.to_csv(outfile, sep = '\t', header = True, index = False)

