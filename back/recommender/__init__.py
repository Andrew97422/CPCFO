import nltk
nltk.download('popular')

from .skills2rec import get_coherence_map, show_coherence_map, plot2image
from .text2skills import SaigaHR
from .rag4opt import vacancy_to_skills_rag

def get_rec_and_image(u):
    '''u - словарь/json/pd.Series, который будет конвертирован в pd.Series и должен иметь поля title и body
        Returns: list(cursees titles), PIL.Image
    '''
    cm = get_coherence_map(u)
    show_coherence_map(cm)
    return cm.index.to_list(), plot2image()

def reccomend(id, title, description, T=0.9):
    u = {'name':id, 'title':title, 'description':description}
    skills = vacancy_to_skills_rag(u, T)
    return get_rec_and_image({'title': title, 'body': skills})