import numpy as np
import pandas as pd


def create_cooccurrence_matrix(cites):
    """Create co occurrence matrix from given list of sentences.

    Returns:
    - vocabs: dictionary of word counts
    - co_occ_matrix_sparse: sparse co occurrence matrix

    Example:
    ===========
    sentences = ['I love nlp',    'I love to learn',
                 'nlp is future', 'nlp is cool']

    vocabs,co_occ = create_cooccurrence_matrix(sentences)

    df_co_occ  = pd.DataFrame(co_occ.todense(),
                              index=vocabs.keys(),
                              columns = vocabs.keys())

    df_co_occ = df_co_occ.sort_index()[sorted(vocabs.keys())]

    df_co_occ.style.applymap(lambda x: 'color: red' if x>0 else '')

    """
    import scipy.sparse as sparse

    arts = {}
    data = []
    row = []
    col = []

    for cite in cites:
        for pos, art in enumerate(cite):
            i = arts.setdefault(art, len(arts))
            start = 0
            end = len(cite)
            for pos2 in range(start, end):
                if pos2 == pos:
                    continue
                j = arts.setdefault(cite[pos2], len(arts))
                data.append(1.)
                row.append(i)
                col.append(j)

    cooccurrence_matrix_sparse = sparse.coo_matrix((data, (row, col)))
    return arts, cooccurrence_matrix_sparse

df = pd.read_csv("./data/cites/Invokabilities-w7ry3boc7fcczbydbhi56dhbqm-dev.csv")
arts = dict()

for index, row in df.iterrows():
    cites = []
    ds = int(row["ds_split (S)"].split("_")[0])
    score = row["scores (S)"]
    score = eval(score)
    for item in score:
        art = item["name"].replace("Article", "").strip()
        label = item["label"]
        if label > 0:
            cites.append(art)

    try:
        arts[str(ds)] += cites
    except KeyError:
        arts[str(ds)] = cites

arts_all = []
for key in list(arts.keys()):
    arts_all.append(arts[key])


vocabs, co_occ = create_cooccurrence_matrix(arts_all)

df_co_occ  = pd.DataFrame(co_occ.todense(),
                          index=vocabs.keys(),
                          columns=vocabs.keys())

df_co_occ = df_co_occ.sort_index()[sorted(vocabs.keys())]

df_co_occ.style.applymap(lambda x: 'color: red' if x>0 else '')

print(df_co_occ)

# normalized_df=(df_co_occ-df_co_occ.min())/(df_co_occ.max()-df_co_occ.min())
n_df_reverse = df_co_occ.sort_index(ascending=False)
data = n_df_reverse.values

# il1 = np.tril_indices(58)
# data[il1] = 0
# n_df_reverse = pd.DataFrame(data=data, columns=n_df_reverse.columns, index=n_df_reverse.index)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(50, 50))
ax.set_title("coo", fontsize=50, pad=30)
ax.set_aspect("equal")

# give some margin between title and heatmap
ttl = ax.title
ttl.set_position([0.5, 1.05])

hmap = plt.pcolor(n_df_reverse, edgecolors="k", linewidths=1)
plt.clim(0, 8)

# cb = plt.colorbar(hmap, shrink=1,  pad=0.01, fraction=0.046)
# cb.ax.tick_params(labelsize=30)
# cb.ax.set_aspect('equal')
plt.yticks(np.arange(0.5, len(n_df_reverse.index), 1), n_df_reverse.index, fontsize=25)
plt.xticks(np.arange(0.5, len(n_df_reverse.columns), 1), n_df_reverse.columns, fontsize=25)
ax.xaxis.tick_top()

plt.savefig(f"./data/cites/plots/coo.png")
plt.show()
# plt.close()

if __name__ == "__main__":
    pass