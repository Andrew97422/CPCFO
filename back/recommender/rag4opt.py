import numpy as np
import pandas as pd
import torch
from sentence_transformers import util
from .text2skills import SaigaHR
from .encode import Encoder

dbU = pd.read_csv('recommender/cache/dbU.csv', index_col=0)
dbembs = torch.load('recommender/cache/dbembs.pt')

def search_in_base(qemb, dbembs):
    sim = util.cos_sim(qemb, dbembs)[0].cpu().numpy()
    best_index = np.argmax(sim)
    return best_index, sim[best_index]

def vacancy_to_skills_rag(u, T=0.9):
    '''u.name = vacancy_id  u.index = ['title',' description']'''
    u = pd.Series(u)
    qemb = Encoder()(u.title + ' ' + u.description)
    best_index, sim = search_in_base(qemb, dbembs)
    if sim >= T:
        return dbembs.iloc[best_index].body
    else:
        output = SaigaHR().vacancy_to_skills(u)
        new_index = u.name if hasattr(u, 'name') else str(dbU.shape[0])+'i'
        dbU.loc[new_index] = output
        dbU.to_csv('recommender/cache/dbU.csv')

        dbembs = torch.cat((dbembs, qemb[None]), 0)
        torch.save(dbembs, 'recommender/cache/dbembs.pt')
        return output
