import pandas as pd
from datetime import timedelta


def handle_excel(file):
    df = pd.read_excel(file)
    df = df[['Work Date', 'Time From', 'Pers No', 'Overall Transports', 'Boxes Picked Picking',
             'Loadings']].sort_values(by=['Work Date', 'Time From'], ascending=[True, True]).reset_index(drop=True)

    def work_shift(row):
        dd = str(row['Time From'])
        h, m, s = dd.split(':')
        h = int(h)

        if h in range(20, 24):
            return row['Work Date'] + timedelta(1)
        else:
            return row['Work Date']

    df['DATE'] = df.apply(work_shift, axis=1)
    final = df.groupby(['Pers No', 'DATE'], sort=True).sum().reset_index()
    final_dict = final.to_dict(orient='records')
    return final_dict
