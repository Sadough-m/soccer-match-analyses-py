import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import shapiro
from scipy import stats

passes_data = pd.read_csv("./passes.csv", header=0, sep=";")
df = pd.DataFrame(passes_data)
df = df[df['passing_quote'].isna() == False].reset_index(drop=True)
print('df',df)


def difference_pass_rate(row):
    match_game_ids = df.index[(df['game_id'] == row["game_id"])].tolist()
    opponent_id = list(filter(lambda x: row.name != x, match_game_ids))[0]
    opponent = df.iloc[opponent_id]
    difference_passes = row['passing_quote'] - opponent['passing_quote']
    return abs(difference_passes)


def map_string_to_bool(value):
    if value == 'Yes':
        return True
    elif value == 'No':
        return False
    else:
        return None  # or whatever default value you prefer


df["winner"] = df["winner"].map(map_string_to_bool).astype(bool)
df['difference_passes'] = df.apply(difference_pass_rate, axis=1)
# passes_data["winner"] = passes_data['winner'].astype(bool)
duplicates_mask = df.duplicated(subset=['game_id', 'winner'], keep=False)
# Filter out rows containing duplicates
exclude_draw_df = df[~duplicates_mask]
exclude_draw_duplicate_mask = exclude_draw_df.duplicated(subset=['game_id'], keep='first')
exclude_draw_df = exclude_draw_df[~exclude_draw_duplicate_mask]

draw_df = df[duplicates_mask]
draw_duplicate_mask = draw_df.duplicated(subset=['game_id'], keep='first')
draw_df = draw_df[~draw_duplicate_mask]

print('exclude_draw_df', exclude_draw_df.describe())
print('draw_df', draw_df.describe())
# print(df[(df["difference_passes"] >0) ].describe())

# # Plot histogram
# plt.figure(figsize=(8, 6))
# sns.histplot(draw_df, x='difference_passes', kde=True, color='lightgreen', bins=30)
# plt.title('Histogram of Draw Games')
# plt.xlabel('difference_passes')
# plt.ylabel('Frequency')
# plt.show()

# # Box plot
# plt.figure(figsize=(8, 6))
# sns.boxplot(draw_df, x='difference_passes', color='lightgreen')
# plt.title('Boxplot of Draw Games ')
# plt.xlabel('difference_passes')
# plt.show()

# Shapiro-Wilk test
stat_winner, p_winner = shapiro(exclude_draw_df['difference_passes'])
stat_draw, p_draw = shapiro(draw_df['difference_passes'])
print('Shapiro-Wilk Test:')
print('stat_winner:', stat_winner,p_winner)
print('stat_losser:', stat_draw,p_draw)
print('p_winner:', p_winner > 0.05)
print('p_draw:', p_draw > 0.05)


u_statistic, p_value = stats.mannwhitneyu(exclude_draw_df['difference_passes'], draw_df['difference_passes'])
print('statistic',u_statistic,p_value)
print('There is a significant difference between difference passes of win games and draw games',p_value < 0.05)