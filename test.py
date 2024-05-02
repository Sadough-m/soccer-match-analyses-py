import pandas as pd

# Create a sample DataFrame
data = {'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)


# Define a function to perform row-wise calculation
def calculate_sum(row):
    return row['A'] + row['B']


# Apply the function to each row to create a new column 'C'
df['C'] = df.apply(calculate_sum, axis=1)

print(df)
