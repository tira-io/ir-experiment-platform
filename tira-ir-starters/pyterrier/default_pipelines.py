import pyterrier as pt
from copy import deepcopy


ALLOWED_PARAMETERS = {
    'RM3': ('fb_terms', 'fb_docs', 'fb_lamdba'),
}


def add_params(controls, params, params_type):
    allowed_parameters = ALLOWED_PARAMETERS[params_type]
    
    for key, value in params.items():
        if key in allowed_parameters:
            controls[key] = value
    
    return controls


def wmodel_batch_retrieve(index_ref, params):
    return pt.BatchRetrieve(index_ref, params)


def wmodel_text_scorer(index_ref, params):
    params = deepcopy(params)
    default_params = {'verbose': True, 'body_attr': 'text'}

    for k,v in default_params.items():
        if params and k not in params:
            params[k] = v

    return pt.text.scorer(**params)


def wmodel_batch_retrieve_rm3(index_ref, params):
    wmodel_retrieve = wmodel_batch_retrieve(index_ref, params)
    rm3 = pt.rewrite.RM3(index_ref, **add_params({}, params, 'RM3'))
    
    return wmodel_retrieve >> rm3 >> wmodel_retrieve

