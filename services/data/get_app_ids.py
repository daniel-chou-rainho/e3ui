def get_app_ids(data):
    return data['AppId'].drop_duplicates().sort_values().tolist()
