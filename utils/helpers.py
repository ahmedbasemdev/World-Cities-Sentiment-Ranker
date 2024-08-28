import json
import datetime

wanted_columns = ["url","id","text","sentiment",'city_id']
def convert_df2json(df):
    df = df[wanted_columns]
    df.loc[:,'type']='tweet'
    list_json = df.to_json(orient='records')
    list_json = json.loads(list_json)
    return list_json


def get_yesterday_str():
  """Gets yesterday's date as a string in the format 'YYYY-MM-DD'."""
  yesterday = datetime.date.today() - datetime.timedelta(days=2)
  return yesterday.strftime('%Y-%m-%d')



