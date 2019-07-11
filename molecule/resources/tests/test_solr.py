import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('solr')

def test_systemd(host):
    s = host.service("solr")

    assert s.is_running
    assert s.is_enabled
