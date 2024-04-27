from .predictor import get_coherence_map, show_coherence_map, plot2image

def get_coherence_map_image_from_skills(request):
    '''u - словарь/json/pd.Series, который будет конвертирован в pd.Series и должен иметь поля title и body'''
    show_coherence_map(get_coherence_map(request))
    return plot2image()