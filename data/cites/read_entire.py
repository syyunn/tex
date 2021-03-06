import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def create_heatmap(df, title="Prediction on Citability"):
    fig, ax = plt.subplots(figsize=(50, 50))
    ax.set_title(title, fontsize=45, pad=50)
    ax.set_aspect("equal")

    ttl = ax.title
    ttl.set_position([0.5, 1.05])

    hmap = plt.pcolor(df, edgecolors="k", linewidths=1)
    plt.clim(0, 1)

    plt.yticks(np.arange(0.5, len(df.index), 1), df.index, fontsize=14)
    df_columns_wo_parenthesis = [col.replace('(', '').replace(')', '').split(':') for col in df.columns.values]
    df_columns_wo_parenthesis = [col[0] + ':' + '\n' + col[1] if len(col) == 2 else col[0] + '\n' + '' for col in df_columns_wo_parenthesis]

    # plt.xticks(np.arange(0.5, len(df.columns), 1), df_columns_wo_parenthesis, fontsize=5)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df_columns_wo_parenthesis, fontsize=9)
    ax.xaxis.tick_top()
    ax.set_ylim((0, len(df.index)))

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="0.5%", pad=0.1)

    cb = fig.colorbar(hmap, orientation="horizontal", cax=cax)
    cb.ax.tick_params(labelsize=25)

    # plt.savefig(f"./data/cites/plots/{title}.png")
    # plt.savefig('./prediction.png', dpi=200)
    plt.savefig('./prediction.svg', format="svg", dpi=200)

    plt.show()
    plt.close()


# df_chronos = pd.read_csv("./data/comps/ds_chronos.csv")
#
# comps_per_ds = {}
# countries = []
# for index, row in df_chronos.iterrows():
#     comps = []
#     ds = row["ds_num"].replace("DS", "")
#     comps_raw = row["comp"].strip()
#
#     if "[" in comps_raw:
#         comps = eval(row["comp"])
#         comps_per_ds[ds] = comps
#         countries += comps
#         continue
#     else:
#         comps.append(row["comp"])
#     comps_per_ds[ds] = comps
#     countries += comps
#
# countries = sorted(list(set(countries)))

df = pd.read_csv("./data/cites/Invokabilities-w7ry3boc7fcczbydbhi56dhbqm-dev.csv")

scores = df["scores (S)"]
dss = df["ds_split (S)"]

# find unique indices
indices = []
for score in scores:
    score = eval(score)
    for item in score:
        indices.append(item["name"].replace("Article", "").strip())

indices = sorted(list(set(indices)))

# indices = ['I', 'I:1', 'II', 'II:1', 'II:1(a)', 'II:1(b)', 'II:2', 'II:3', 'III',
#        'III:1', 'III:2', 'III:4', 'III:5', 'IX', 'IX:2', 'V:6', 'VI', 'VI:1',
#        'VI:2', 'VI:2(a)', 'VI:2(b)', 'VI:3', 'VI:6', 'VII', 'VII:1', 'VII:2',
#        'VII:5', 'VIII', 'VIII:1', 'VIII:4', 'X', 'X:1', 'X:2', 'X:3', 'X:3(a)',
#        'XI', 'XI:1', 'XIII', 'XIII:1', 'XIII:2', 'XIX', 'XIX:1', 'XIX:2', 'XV',
#        'XVI', 'XVI:1', 'XVII', 'XVII:1', 'XVIII:11', 'XX', 'XXII', 'XXII:1',
#        'XXIII', 'XXIII:1', 'XXIII:1(a)', 'XXIII:1(b)', 'XXIV', 'XXVIII']

# find unique dss
columns = []
for ds in dss:
    ds_num = ds.split("_")[0]
    columns.append(int(ds_num))

dss = sorted(list(set(columns)), reverse=True)
dss = ['DS ' + str(ds) for ds in dss]


# dss_nrv = sorted(list(set(columns)))

# cites_nrv = DataFrame(
#     abs(np.random.randn(len(dss_nrv), len(indices))), index=dss_nrv, columns=indices
# )

cites = DataFrame(
    np.zeros((len(dss), len(indices))),
    index=dss,
    columns=indices
)

# errors = DataFrame(
#     abs(np.random.randn(len(dss), len(indices))),
#     index=dss,
#     columns=indices,
# )
#
# errors_discrete = DataFrame(
#     np.zeros((len(dss), len(indices))),
#     index=dss,
#     columns=indices,
# )
#
# labels = DataFrame(
#     abs(np.random.randn(len(dss), len(indices))),
#     index=dss,
#     columns=indices,
# )

for index, row in df.iterrows():
    ds = int(row["ds_split (S)"].split("_")[0])
    score = row["scores (S)"]
    score = eval(score)

    for item in score:
        art = item["name"].replace("Article", "").strip()
        if art in indices:
            pred = item["pred"]
            # label = item["label"]
            # error = abs(pred - label)
            # error_disc = abs(round(pred) - label)

            cites.at['DS ' + str(ds), art] = pred
            # cites_nrv.at[ds, art] = round(pred, 2)
            # errors.at[ds, art] = error
            # errors_discrete.at[ds, art] = error_disc
            # labels.at[ds, art] = label
        else:
            pass

# create_heatmap(dss, indices, df=errors_discrete, title=f"Error")
# create_heatmap(dss, indices, df=errors, title='Errors')
# create_heatmap(dss, indices, df=errors_discrete, title=f'{country} Errors')
# create_heatmap(dss, indices, df=labels, title='Labels')
# break

# cites_nrv.to_csv('./cites_nrv.csv')
# cites.to_csv('./cites.csv', index=False, sep='\t')

print("")
create_heatmap(df=cites, title='Prediction')
# create_heatmap(dss, indices, df=errors, title='Errors')
# create_heatmap(dss, indices, df=errors_discrete, title='Errors')
# create_heatmap(dss, indices, df=labels, title='Labels')


if __name__ == "__main__":
    pass
