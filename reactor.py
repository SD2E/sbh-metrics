import configparser
import json
import os

from reactors.runtime import Reactor
from reactors.runtime import agaveutils

# Import the inappropriately named sbh-metrics.py
# TODO: rename sbh-metrics.py so it can be imported
import importlib
sbhmetrics = importlib.import_module('sbh-metrics')


def load_metrics_config(config_path):
    """Load the metrics configuration so certain values can be accessed"""
    # What we really need is the output directory: csv_writer.out_dir
    config = configparser.ConfigParser()
    with open(config_path) as fp:
        config.read_file(fp)
    return config


# Should use bacanora for this. https://github.com/SD2E/bacanora
def download_file():
    # bacanora.download(client, remote_file, local_file, system_id)
    pass


def download_metrics_files(agave_client, agave_sys, agave_dir, dest_dir, logger):
    """Download all the existing metrics files from their permanent store."""
    # List the directory (agave_client.files.list(agave_sys, agave_dir))
    logger.info('agave_client type is %r', type(agave_client))
    logger.info('agave_client.files type is %r', type(agave_client.files))
    for x in dir(agave_client.files):
        logger.info('Found agave_client.files.%s', x)
    filenames = agave_client.files.list(systemId=agave_sys, filePath=agave_dir)
    logger.info('filenames type is %r', type(filenames))
    for f in filenames:
        logger.info('Found file %s', f)
    #
    # For each file:
    #    construct agave_path
    #    construct dest_path
    #    download_file(agave_client, agave_path, dest_path, agave_sys)


def main():
    r = Reactor()
    r.logger.info("Hello this is actor {}".format(r.uid))
    md = r.context.message_dict
    r.logger.info(json.dumps(md))

    # Extract config file from settings
    metrics_conf_file = r.settings.metrics.config
    metrics_config = load_metrics_config(metrics_conf_file)
    # Dig out csv_writer out_dir
    metrics_dir = metrics_config.get('csv_writer', 'out_dir')

    # Download all files from agave to metrics_dir

    # Get Agave info
    agave_uri = md.get('uri')
    r.logger.info('Agave URI: %s', agave_uri)
    agave_sys, agave_path, agave_file = agaveutils.from_agave_uri(agave_uri)
    download_metrics_files(r.client, agave_sys, agave_path, metrics_dir,
                           r.logger)
    r.logger.info('download complete')
    return None

    file_to_download = os.path.join(agave_path, 'TriplesMetric.csv')
    rsp = r.client.files.download(systemId=agave_sys, filePath=file_to_download)
    if isinstance(rsp, dict):
        # An error occurred
        r.logger.info('Agave error: %r', rsp)
        return 1

    # Write the data from the response out to disk
    with open('TriplesMetric.csv', 'wb') as f:
        for block in rsp.iter_content(2048):
            if not block:
                break
            r.logger.info('Block type is %r', type(block))
            if len(block) > 10:
                r.logger.info('First 10: %r', block[:10])
            f.write(block)
    return 2


    # SynBioHub settings are passed via secrets.json
    r.logger.info('Getting synbiohub settings')
    sbh_settings = r.settings.get('sbh', {})
    sbh_user = sbh_settings['user']
    sbh_password = sbh_settings['password']
    r.logger.info('SynBioHub user: %s', sbh_user)
    r.logger.info('SynBioHub password is available')

    sbhm_args = ['-u', sbh_user, '-p', sbh_password, '/reactor.ini']
    r.logger.info('Invoking sbh metrics with %r', sbhm_args)
    sbhmetrics.main(sbhm_args)


if __name__ == '__main__':
    main()
