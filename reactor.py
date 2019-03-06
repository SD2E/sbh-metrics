import configparser
import json
import os

import bacanora
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


def download_metrics_files(agave_client, agave_sys, agave_dir, dest_dir,
                           logger):
    """Download all the existing metrics files from their permanent store."""
    filenames = agave_client.files.list(systemId=agave_sys, filePath=agave_dir)
    for f in filenames:
        if f.name == '.':
            # Skip the directory itself
            continue
        local_path = os.path.join(dest_dir, f.name)
        local_file = bacanora.download(agave_client, f.path, local_path,
                                       system_id=f.system)
        logger.info('Downloaded %s from Agave', f.name)


def upload_metrics_files(agave_client, agave_sys, agave_dir, src_dir, logger):
    filenames = os.listdir(src_dir)
    for f in filenames:
        src_path = os.path.join(src_dir, f)
        logger.info('Uploading %s to %s:%s', src_path, agave_sys, agave_dir)
        # bacanora.upload(agave_client, src_path, agave_dir,
        #                 system_id=agave_sys, autogrant=True)

        # see https://github.com/SD2E/bacanora/issues/1
        bacanora.upload(agave_client, src_path, agave_dir,
                        system_id=agave_sys, autogrant=False)

        grant_path = os.path.join(agave_dir, f)
        logger.info('granting on %s', grant_path)
        bacanora.grant(agave_client, grant_path, agave_sys)
        logger.info('Uploaded %s to Agave', f)


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
    try:
        os.makedirs(metrics_dir)
    except FileExistsError:
        pass

    # Get Agave info
    agave_uri = md.get('uri')
    r.logger.info('Agave URI: %s', agave_uri)
    agave_sys, agave_path, agave_file = agaveutils.from_agave_uri(agave_uri)

    # Download all files from agave to metrics_dir
    download_metrics_files(r.client, agave_sys, agave_path, metrics_dir,
                           r.logger)

    # SynBioHub settings (user, password) are passed via secrets.json
    r.logger.info('Getting synbiohub settings')
    sbh_settings = r.settings.get('sbh', {})
    sbh_user = sbh_settings['user']
    sbh_password = sbh_settings['password']
    r.logger.info('SynBioHub user: %s', sbh_user)
    r.logger.info('SynBioHub password is available')

    sbhm_args = ['-u', sbh_user, '-p', sbh_password, '/reactor.ini']
    # r.logger.info('Invoking sbh metrics with %r', sbhm_args)
    sbhmetrics.main(sbhm_args)

    # Upload the metrics files to Agave
    upload_metrics_files(r.client, agave_sys, agave_path, metrics_dir,
                         r.logger)


if __name__ == '__main__':
    main()
