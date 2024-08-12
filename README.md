[![tests](https://github.com/boutetnico/ansible-role-netdata/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-netdata/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.netdata-blue.svg)](https://galaxy.ansible.com/boutetnico/netdata)

ansible-role-netdata
====================

This role installs and configures [Netdata](https://learn.netdata.cloud/).

Requirements
------------

Ansible 2.15 or newer.

Supported Platforms
-------------------

- [Debian - 11 (Bullseye)](https://wiki.debian.org/DebianBullseye)
- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                         | Required | Default                | Choices   | Comments                                          |
|----------------------------------|----------|------------------------|-----------|---------------------------------------------------|
| netdata_dependencies             | true     |                        | list      | See `defaults/main.yml`.                          |
| netdata_package_state            | true     | `present`              | string    |                                                   |
| netdata_pip_packages             | true     | `[]`                   | list      | Extra pip packages to install.                    |
| netdata_user_extra_groups        | true     | `[]`                   | list      | Extra Unix groups for the Netdata user.           |
| netdata_directory_cache          | true     | `/var/cache/netdata`   | string    |                                                   |
| netdata_streaming_enabled        | true     | `false`                | bool      |                                                   |
| netdata_node_role                | true     | `master`               | string    | Possible values: `master`, `slave`.               |
| netdata_master_api_key           | true     | `change-me-uuid`       | string    |                                                   |
| netdata_master_endpoint          | true     | `''`                   | string    |                                                   |
| netdata_go_d_conf                | true     | `[]`                   | list      |                                                   |
| netdata_python_d_conf            | true     | `[]`                   | list      |                                                   |
| netdata_health_d_conf            | true     | `[]`                   | list      |                                                   |
| netdata_conf                     | true     | `{}`                   | dict      |                                                   |
| netdata_apps_groups              | true     | `{}`                   | dict      |                                                   |
| netdata_alarm_notify             | true     | `{}`                   | dict      |                                                   |
| netdata_alarm_notify_scripts     | true     | `''`                   | string    |                                                   |
| netdata_plugins_path             | true     | `/usr/libexec/netdata` | string    |                                                   |
| netdata_external_plugins_path    | true     | `''`                   | string    |                                                   |
| netdata_external_plugins_install | true     | `[]`                   | list      |                                                   |


Dependencies
------------

None

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-netdata

          netdata_go_d_conf:
            - name: mysql
              config:
                update_every: 10
                autodetection_retry: 60
                jobs:
                  - name: local
                    dsn: "netdata:netdata@tcp(127.0.0.1:3306)/"
            - name: nginx
              config:
                update_every: 10
                autodetection_retry: 60
                jobs:
                  - name: local
                    url: "http://127.0.0.1/nginx_status"

          netdata_python_d_conf:
            - name: memcached
              config:
                update_every: 10
                autodetection_retry: 60


          netdata_health_d_conf:
            - name: ram
              config:
                - template: "ram_in_use"
                  "on": "system.ram"
                  class: "Utilization"
                  type: "System"
                  component: "Memory"
                  host labels: "_hostname = !web01 *"
                  calc: "$used * 100 / ($used + $cached + $free + $buffers)"
                  units: "%"
                  every: "10s"
                  warn: "$this > (($status >= $WARNING)  ? (80) : (90))"
                  delay: "down 15m multiplier 1.5 max 1h"
                  summary: "System memory utilization"
                  info: "System memory utilization"
                  to: "sysadmin"

          netdata_conf:
            global:
              update every: 10
            db:
              mode: "{{ 'dbengine' if netdata_node_role == 'master' else 'none' }}"
            directories:
              cache: "{{ netdata_directory_cache }}"
            logs:
              errors flood protection period: 0
            health:
              enabled: "{{ 'yes' if netdata_node_role == 'master' else 'no' }}"
            ml:
              enabled: "no"
            web:
              enable gzip compression: "no"
            plugins:
              timex: "yes"
              idlejitter: "no"
              netdata monitoring: "no"
              profile: "no"
              tc: "no"
              diskspace: "yes"
              proc: "yes"
              cgroups: "no"
              enable running new plugins: "no"
              slabinfo: "no"
              apps: "yes"
              systemd-journal: "no"
              debugfs: "no"
              ioping: "no"
              python.d: "yes"
              nfacct: "no"
              perf: "yes"
              charts.d: "no"
              go.d: "yes"
              statsd: "no"


Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
