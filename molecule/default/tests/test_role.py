import pytest


@pytest.mark.parametrize(
    "name",
    [
        ("netdata"),
    ],
)
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize(
    "username,groupname,path",
    [
        ("root", "root", "/etc/netdata/netdata.conf"),
        ("root", "root", "/etc/netdata/health_alarm_notify.conf"),
        ("root", "root", "/etc/netdata/apps_groups.conf"),
    ],
)
def test_netdata_config_file(host, username, groupname, path):
    config = host.file(path)
    assert config.exists
    assert config.is_file
    assert config.user == username
    assert config.group == groupname


@pytest.mark.parametrize(
    "name",
    [
        ("netdata"),
    ],
)
def test_service_is_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize(
    "marker",
    [
        ("migrated from:"),
        ("reformatted from:"),
        ("found in the config file, but is not used"),
    ],
)
def test_netdata_conf_has_no_deprecated_markers(host, marker):
    conf = host.file("/etc/netdata/netdata.conf").content_string
    assert marker not in conf, f"netdata.conf contains '{marker}'"
