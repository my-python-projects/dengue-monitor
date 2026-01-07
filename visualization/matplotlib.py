import matplotlib.pyplot as plt

def plot_cases_by_month_matplotlib(df):
    plt.figure()
    plt.plot(df["mes"], df["casos"])
    plt.title("Casos de Dengue por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Casos")
    plt.tight_layout()
    plt.show()
