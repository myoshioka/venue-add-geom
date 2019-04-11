import os
import sys
from dotenv import load_dotenv
import pandas as pd
import click

dotenv_path = './.env'
load_dotenv(dotenv_path)

from lib.log import logging
from lib.foursquare_api import FoursquareApi

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.command()
@click.option('--file-name', '-f',  help='input csv file')
def main(file_name):

    logger.debug('start!')
    df = pd.read_csv(file_name)
    out_list = []
    for index, row in df.iterrows():
        venue_id = row['current_venue_id']
        print(venue_id)
        venues_detail = FoursquareApi.get_foursquare_venue_details(venue_id)

        state = None
        city = None
        address = None
        if 'state' in venues_detail['location']:
            state = venues_detail['location']['state']

        if 'city' in venues_detail['location']:
            city = venues_detail['location']['city']

        if 'address' in venues_detail['location']:
            address = venues_detail['location']['address']

        out_list.append([
            index, venues_detail['name'],
            venues_detail['location']['lat'],
            venues_detail['location']['lng'],
            state,
            city,
            address
        ])

    out_venue_df = pd.DataFrame(
        out_list, columns=['id', 'venue_name', 'lat', 'lng', 'state', 'city', 'address'])

    out_df = pd.merge(df, out_venue_df, how='left',
                      left_index=True, right_index=True)
    out_df.to_csv('./' + file_name.replace('.csv', '') + '_add_location.csv')

    logger.debug('end!')


if __name__ == '__main__':
    main()
