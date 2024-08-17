import json

wanted_columns = ["url","id","text","createdAt","sentiment",'city_id']
def convert_df2json(df):
    df = df[wanted_columns]
    df['type']='tweet'
    list_json = df.to_json(orient='records')
    list_json = json.loads(list_json)
    return list_json



