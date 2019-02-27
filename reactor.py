import json
import os

from reactors.runtime import Reactor


def main():
    r = Reactor()
    r.logger.info("Hello this is actor {}".format(r.uid))
    md = r.context.message_dict
    r.logger.info(json.dumps(md))

    # SynBioHub settings are passed via secrets.json
    r.logger.info('Getting synbiohub settings')
    sbh_settings = r.settings.get('sbh', {})
    sbh_user = sbh_settings['user']
    sbh_password = sbh_settings['password']
    r.logger.info('SynBioHub user: %s', sbh_user)
    r.logger.info('SynBioHub password is available')

if __name__ == '__main__':
    main()
