import pandas as pd
from scipy.stats import shapiro
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

passes_data = pd.read_csv("./passes.csv", header=0, sep=";")
df = pd.DataFrame(passes_data)
df = df[df['passing_quote'].isna() == False].reset_index(drop=True)

print('df',df.describe())


def map_string_to_bool(value):
    if value == 'Yes':
        return True
    elif value == 'No':
        return False
    else:
        return None  # or whatever default value you prefer


df["winner"] = df["winner"].map(map_string_to_bool).astype(bool)

# Identify duplicate rows based on specific columns
duplicates_mask = df.duplicated(subset=['game_id', 'winner'], keep=False)
# Filter out rows containing duplicates
exclude_draw_df = df[~duplicates_mask]
draw_df = df[duplicates_mask]

winner_df = exclude_draw_df[(df['winner'] == True)]
losser_df = exclude_draw_df[(df['winner'] == False)]

print(winner_df.describe())
print(losser_df.describe())

# # Plot histogram
# plt.figure(figsize=(8, 6))
# sns.histplot(draw_df, x='passing_quote', kde=True, color='lightgreen', bins=30)
# plt.title('Histogram of Draw Games')
# plt.xlabel('passing_quote')
# plt.ylabel('Frequency')
# plt.show()
# # Box plot
# plt.figure(figsize=(8, 6))
# sns.boxplot(winner_df, x='passing_quote', color='lightgreen')
# plt.title('Boxplot of Winners ')
# plt.xlabel('passing_quote')
# plt.show()

# Shapiro-Wilk test
stat_winner, p_winner = shapiro(winner_df['passing_quote'])
stat_losser, p_losser = shapiro(losser_df['passing_quote'])
print('Shapiro-Wilk Test:')
print('stat_winner:', stat_winner)
print('stat_losser:', stat_losser)
print('p_winner:', p_winner > 0.05)
print('p_losser:', p_losser > 0.05)

u_statistic, p_value = stats.mannwhitneyu(winner_df['passing_quote'], losser_df['passing_quote'])
print('statistic',u_statistic)
print('There is a significant difference between passing rates of winners and losers',p_value < 0.05)