import os
import sys
from dotenv import load_dotenv
import pandas as pd

dotenv_path = './.env'
load_dotenv(dotenv_path)

from lib.log import logging
from lib.foursquare_api import FoursquareApi

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():

    logger.debug('start!')
    df = pd.read_csv('./poi_ranking.csv')
    out_list = []
    for index, row in df.iterrows():
        venue_id = row['current_venue_id']
        print(venue_id)
        venues_detail = FoursquareApi.get_foursquare_venue_details(venue_id)
        out_list.append([index, venues_detail['name'], venues_detail['location']['lat'],
                         venues_detail['location']['lng']])

    out_venue_df = pd.DataFrame(
        out_list, columns=['id', 'venue_name', 'lat', 'lng'])

    out_df = pd.merge(df, out_venue_df, how='left',
                      left_index=True, right_index=True)
    out_df.to_csv('./poi_ranking_location.csv')

    logger.debug('end!')


if __name__ == '__main__':
    main()
