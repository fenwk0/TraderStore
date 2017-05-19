#!/bin/env python
# -*- coding: UTF-8 -*-

from flask import json
import os

def generate_swagger(app_name, instance, fp):
    """Initialize an instance of the application API, then use its
    context to generate a json schema and dump to disk as 'swagger.json'
    """

    app_loc = app_name + '_app'
    inst_loc = instance + '_instance'

    # Dynamically generate module names for import
    import_statement = "from {}.application import create_application, get_api"
    exec(import_statement.format(app_loc))

    print(
        'Generating swagger.json file for {} instance of {} application'.format(inst_loc, app_name)
    )

    app = create_application(os.path.abspath(inst_loc))
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
    parser.add_argument('application', choices=['market', 'reporting'])
    parser.add_argument('instance', choices=['potato', 'carrot', 'reporting'])
    parser.add_argument('-o', '--outfile', default='swagger.json', help="filename for json output of swagger schema")
    args = parser.parse_args()

    generate_swagger(app_name=args.application, instance=args.instance, fp=args.outfile)
