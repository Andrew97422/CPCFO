from .skills2rec import get_coherence_map, show_coherence_map, plot2image
from .text2skills import SaigaHR

def get_rec_and_image(request):
    '''u - словарь/json/pd.Series, который будет конвертирован в pd.Series и должен иметь поля title и body
        Returns: list(cursees titles), PIL.Image
    '''
    cm = get_coherence_map(request)
    show_coherence_map(cm)
    return cm.index.to_list(), plot2image()

def get_skills_from_text(text):
    return SaigaHR().vacancy_to_skills(text)