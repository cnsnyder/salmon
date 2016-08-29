#! /usr/bin/env python
from __future__ import absolute_import

import os
import unittest
import salmon
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)5s [%(name)s:%(lineno)s] %(message)s")
logger = logging.getLogger('')
logger.setLevel(logging.INFO)


class SalmonConfig(unittest.TestCase):
    def setUp(self):
        self.good_config = {
            'repos': {
                'rhel7_2': {
                    'url': 'http://download.eng.rdu2.redhat.com/released/RHEL-7/7.2/Server/x86_64/os/'
                }
            },
            'destination': '/var/lib/machines',
            'name': 'RHEL7_2-base',
            'packages': ['systemd', 'passwd', 'vim-minimal', 'redhat-release', 'yum']
        }

    def test_validate_required_with_missing_sections(self):
        s = salmon.Salmon()
        bad_config = {'repos': {}, 'destination': ''}
        with self.assertRaises(RuntimeError):
            s.validate_config(bad_config)

    def test_validate_required_with_missing_repos(self):
        s = salmon.Salmon()
        bad_config = {'repos': {}, 'destination': '', 'name': '', 'packages': []}
        with self.assertRaisesRegexp(RuntimeError, 'No repos'):
            s.validate_config(bad_config)

    def test_validate_required_with_good_config(self):
        s = salmon.Salmon()
        s.validate_config(self.good_config)

    def test_cli_overrides_config_destination(self):
        args = ['--destination', os.getcwd()]
        s = salmon.Salmon(args)
        result_config = s.validate_config(self.good_config)
        self.assertEqual(os.getcwd(), result_config['destination'])


if __name__ == "__main__":
    unittest.main(module="salmon")