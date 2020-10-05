import pandas as pd

df = pd.read_csv('./data/comps/ds_chronos.csv')

comps_per_ds = {}
countries = []
for index, row in df.iterrows():
    comps = []
    ds = row['ds_num'].replace('DS', '')
    comps_raw = row['comp'].strip()

    if '[' in comps_raw:
        comps = eval(row['comp'])
        comps_per_ds[ds] = comps
        countries += comps
        continue
    else:
        comps.append(row['comp'])
    comps_per_ds[ds] = comps
    countries += comps

# inv_map = {v: k for k, v in comps.items()}
countries = sorted(list(set(countries)))
if __name__ == "__main__":
    pass
