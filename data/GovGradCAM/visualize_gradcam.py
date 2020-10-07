import pandas as pd
import datetime
import pickle

pkl = '/Users/suyeol/tex/data/GovGradCAM/GovGradCAM.pkl'

start = datetime.datetime.now()

import pickle
with open(pkl, 'rb') as pickle_file:
    try:
        while True:
            article = pickle.load(pickle_file)
            print(article)
    except EOFError:
        print("EOFError")
        pass
end = datetime.datetime.now()

print(start-end)

if __name__ == "__main__":
    pass
