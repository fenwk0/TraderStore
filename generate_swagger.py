#!/bin/env python
# -*- coding: UTF-8 -*-

from flask import json

from market_app.application import create_application, get_api

def generate_swagger(fp):
    """Initialize an instance of the application API, then use its
    context to generate a json schema and dump to disk as 'swagger.json'
    """
    print('Generating swagger.json file')
    app = create_application()
    api = get_api()

    # Required to make sure the app is able to create a URL adapter for
    # request independent URL generation. Otherwise a RuntimeError is
    # raised
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        with open(fp, 'wb') as fh:
            json.dump(api.__schema__, fh)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-o', '--outfile', default='swagger.json', help="filename for json output of swagger schema")
    args = parser.parse_args()

    generate_swagger(fp=args.outfile)
