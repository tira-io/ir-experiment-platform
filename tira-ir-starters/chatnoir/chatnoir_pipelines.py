from tira.third_party_integrations import get_preconfigured_chatnoir_client

def retrieve_by_default_text(index_ref, controls):
    return get_preconfigured_chatnoir_client(config_directory = controls['raw_passed_arguments']['input'], features = [], verbose = True, num_results=1000, page_size=1000)

