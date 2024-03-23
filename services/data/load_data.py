import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()
    data['TimeStamp'] = pd.to_datetime(data['TimeStamp'].str.strip(), format='%Y-%m-%d:%H:%M:%S.%f')
    return data