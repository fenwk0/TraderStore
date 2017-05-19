from flask import current_app
from flask_restplus import Resource, Namespace, abort

import swagger_client

from swagger_client.rest import ApiException

report_ns = Namespace('report_ns', description='Report namespace')


def get_book_instrument(api_instance):

    book = api_instance.get_book_view()
    return book.instrument


def get_book_stats(api_instance):
    stats = api_instance.get_book_stats_view()
    exported_keys = ['offer_price', 'bid_price', 'spread', 'trade_count']
    return [{key: getattr(stats, key) for key in exported_keys}]


class StatReportResource(Resource):

    def get(self):

        results = {}
        for host in current_app.config['MARKET_SERVICES']:
            # create an instance of the API class
            client = swagger_client.ApiClient(host=host)
            api_instance = swagger_client.BookNsApi(api_client=client)

            host_instrument = get_book_instrument(api_instance)
            stats = get_book_stats(api_instance)

            # Two services with the same instrument will clash!
            results[host_instrument] = stats

        return results


@report_ns.errorhandler(ApiException)
def handle_api_exception(error):
    """ Return a custom message for ApiException errors. """
    return {
        'message': 'Error contacting on of the market services: {}'.format(error)
    }, 500


report_ns.add_resource(StatReportResource, '/reports/stats')
