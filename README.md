Solr configuration as a Cloud
=========
[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-solr_cloud/master/LICENSE)
[![Build Status](https://travis-ci.org/lean-delivery/ansible-role-solr_cloud.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-solr_cloud)
[![Build Status](https://gitlab.com/lean-delivery/ansible-role-solr_cloud/badges/master/build.svg)](https://gitlab.com/lean-delivery/ansible-role-solr_cloud)
[![Galaxy](https://img.shields.io/badge/galaxy-lean__delivery.solr__cloud-blue.svg)](https://galaxy.ansible.com/lean_delivery/solr_cloud)
![Ansible](https://img.shields.io/ansible/role/d/role_id.svg)
![Ansible](https://img.shields.io/badge/dynamic/json.svg?label=min_ansible_version&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2Frole_id%2F&query=$.min_ansible_version)

This role:
  - Configure Solr instances as cloud.
  - Upload Solr configsets config to zookeeper


Requirements
------------
- Minimal Version of the ansible for installation: 2.5
  - **Java 8** [![Build Status](https://travis-ci.org/lean-delivery/ansible-role-java.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-java)
  - **Zookeper** cluster installed [![Build Status](https://travis-ci.org/lean-delivery/ansible-role-zookeeper.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-zookeeper)
  - ** Solr** standalone servers installed [![Build Status](https://travis-ci.org/lean-delivery/ansible-role-solr-standalone.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-solr-standalone)
  - Zookeeper(z)-solr(s) instances formula should be s=2z+1 or s=z+1
  - **Supported OS**:
    - CentOS
      - 7
    - Ubuntu
    - Debian

Role Variables
--------------
 - `solr_version` - installed solr version default: `7.1.0`
 - `solr_insh_default` - solr in.sh folder default: `/etc/default/solr.in.sh`
 - `solr_service_name` - solr service name default: `solr`
 - `solr_base_path` - path to solr base default: `/var/solr`
 - `solr_home` - path to SOLR_HOME default: `{{ solr_base_path }}/data`
 - `dest_main_path` - root directory to store solr folder default: `/opt`
 - `dest_solr_path` - solr folder path default: `{{ dest_main_path }}/solr-{{ solr_version }}`
 - `solr_configset_path` - path to configsets default: `{{ solr_home }}/configsets`
 - `solr_binary` - path to solr binary default: `"{{ dest_solr_path }}/bin/solr"`

 # Solr Cloud variables
   - `zk_inventory_group` - zookeeper inventory group. If not empty and the group exists - solr cloud mode enabled.
     default: `''`
   - `zk_client_port` - zookeeper port
     default: `2181
   - `configset_list` - list of configset directories
     default: `- default`
   - `auto_populate_configset_list` - get all configset directories automatically
     default: `True`
   - `zk_enable_ssl` - set zookeepers to communicate with solr by ssl
      default: `True`
   - `zk_hosts_list` - list of zookeeper hosts
      default: `{{ groups[zk_inventory_group] | map("extract", hostvars, ["ansible_default_ipv4","address"]) | list }}`
   - `solr_host_naming` - solr host name - to set FQDN name - solr will be reached for zookeeper by this name or ip
      default: `{{ ansible_fqdn }}`

Example Inventory
----------------
```ini
 [solr]
 solr.example.com
 solr2.example.com

 [zookeeper]
 zookeeper1
 zookeeper2
 zookeeper3
 ```

Example Playbook
----------------

```yml
- name: Install and Configure Zookeeper Cluster
  hosts: zookeeper
  roles:
    - role: lean_delivery.java
    - role: lean_delivery.zookeeper

- name: Install and Configure Solr Servers
  hosts: solr
  vars:
    solr_version: 7.1.0
    solr_change_default_password: False
  roles:
    - role: lean_delivery.java
    - role: lean_delivery.solr_standalone
      solr_ssl_check_peer_name: 'false'
    - role: lean_delivery.solr_cloud
      zk_inventory_group: zookeeper
      configset_list:
        - default
      auto_populate_configset_list: False
```

```yml
- name: Install and Configure Zookeeper Cluster
  hosts: zookeeper
  roles:
    - role: lean_delivery.java
    - role: lean_delivery.zookeeper

- name: Install and Configure Solr Servers without ssl and authentication
  hosts: solr
  vars:
    solr_version: 7.1.0
  roles:
    - role: lean_delivery.java
    - role: lean_delivery.solr_standalone
      solr_change_default_password: False
      solr_auth_configure: False
      solr_ssl_configure: False
    - role: lean_delivery.solr_cloud
      zk_inventory_group: zookeeper
      configset_list:
        - default
      auto_populate_configset_list: False
      zk_enable_ssl: False
```

License
-------

Apache

Author Information
------------------

authors:
  - Lean Delivery Team <team@lean-delivery.com>
