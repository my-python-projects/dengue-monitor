import seaborn as sns

def plot_cases_by_month_seaborn(df):
    sns.lineplot(data=df, x="mes", y="casos", marker="o")
