import numpy as np
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
#
# fig, ax = plt.subplots()
# ax.xaxis.tick_top() # x axis on top
#
Index= ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
Cols = ['A', 'B', 'C', 'D']
# df = DataFrame(abs(np.random.randn(5, 4)), index=Index, columns=Cols)
#
# sns.heatmap(df, annot=True)
# plt.show()
# ax.xaxis.tick_top() # x axis on top


def create_heatmap(index, cols, df=None):
    fig, ax = plt.subplots(figsize=(60, 60))
    if not df:
        df = DataFrame(abs(np.random.randn(len(index), len(cols))), index=index, columns=cols)
    plt.pcolor(df)
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
    ax.xaxis.tick_top()  # x axis on top

    plt.show()


if __name__ == "__main__":
    create_heatmap(index=Cols, cols=Cols)
    pass
