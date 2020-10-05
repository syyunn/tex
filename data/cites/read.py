import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt


def create_heatmap(index, cols, df, title="Prediction on Citability"):
    row_num = len(df)
    fig, ax = plt.subplots(figsize=(50, 50))
    ax.set_title(title, fontsize=50, pad=30)
    ax.set_aspect("equal")

    # give some margin between title and heatmap
    ttl = ax.title
    ttl.set_position([0.5, 1.05])

    hmap = plt.pcolor(df, edgecolors="k", linewidths=1)
    plt.clim(0, 1)

    # cb = plt.colorbar(hmap, shrink=1,  pad=0.01, fraction=0.046)
    # cb.ax.tick_params(labelsize=30)
    # cb.ax.set_aspect('equal')
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index, fontsize=16)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns, fontsize=15)
    ax.xaxis.tick_top()

    plt.savefig(f"./data/cites/plots/{title}.png")
    plt.show()
    plt.close()


df_chronos = pd.read_csv("./data/comps/ds_chronos.csv")

comps_per_ds = {}
countries = []
for index, row in df_chronos.iterrows():
    comps = []
    ds = row["ds_num"].replace("DS", "")
    comps_raw = row["comp"].strip()

    if "[" in comps_raw:
        comps = eval(row["comp"])
        comps_per_ds[ds] = comps
        countries += comps
        continue
    else:
        comps.append(row["comp"])
    comps_per_ds[ds] = comps
    countries += comps

countries = sorted(list(set(countries)))

df = pd.read_csv("./data/cites/Invokabilities-w7ry3boc7fcczbydbhi56dhbqm-dev.csv")

scores = df["scores (S)"]
dss = df["ds_split (S)"]

# find unique indices
indices = []
for score in scores:
    score = eval(score)
    for item in score:
        indices.append(item["name"].replace("Article", ""))

indices = sorted(list(set(indices)))

# find unique dss
columns = []
for ds in dss:
    ds_num = ds.split("_")[0]
    columns.append(int(ds_num))

dss = sorted(list(set(columns)), reverse=True)
dss_nrv = sorted(list(set(columns)))


for country in countries:
    ctn_specific_dss = []
    for ds in dss:
        if country in comps_per_ds[str(ds)]:
            ctn_specific_dss.append(ds)

    if len(ctn_specific_dss) == 0:
        continue
    cites = DataFrame(
        abs(np.random.randn(len(ctn_specific_dss), len(indices))),
        index=ctn_specific_dss,
        columns=indices,
    )

    # cites_nrv = DataFrame(
    #     abs(np.random.randn(len(dss_nrv), len(indices))), index=dss_nrv, columns=indices
    # )

    errors = DataFrame(
        abs(np.random.randn(len(ctn_specific_dss), len(indices))),
        index=ctn_specific_dss,
        columns=indices,
    )

    errors_discrete = DataFrame(
        abs(np.random.randn(len(ctn_specific_dss), len(indices))),
        index=ctn_specific_dss,
        columns=indices,
    )

    labels = DataFrame(
        abs(np.random.randn(len(ctn_specific_dss), len(indices))),
        index=ctn_specific_dss,
        columns=indices,
    )

    for index, row in df.iterrows():
        ds = int(row["ds_split (S)"].split("_")[0])

        if ds in ctn_specific_dss:
            score = row["scores (S)"]
            score = eval(score)
            for item in score:
                art = item["name"].replace("Article", "")
                pred = item["pred"]
                label = item["label"]
                error = abs(pred - label)
                error_disc = abs(round(pred) - label)

                cites.at[ds, art] = pred
                # cites_nrv.at[ds, art] = round(pred, 2)
                errors.at[ds, art] = error
                errors_discrete.at[ds, art] = error_disc
                labels.at[ds, art] = label

    create_heatmap(ctn_specific_dss, indices, df=cites, title=f"{country}'s Prediction")
    # create_heatmap(dss, indices, df=errors, title='Errors')
    # create_heatmap(dss, indices, df=errors_discrete, title=f'{country} Errors')
    # create_heatmap(dss, indices, df=labels, title='Labels')
    # break

# cites_nrv.to_csv('./cites_nrv.csv')

# create_heatmap(dss, indices, df=cites, title='Prediction')
# create_heatmap(dss, indices, df=errors, title='Errors')
# create_heatmap(dss, indices, df=errors_discrete, title='Errors')
# create_heatmap(dss, indices, df=labels, title='Labels')


if __name__ == "__main__":
    pass
