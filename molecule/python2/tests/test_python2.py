"""Module containing the tests for the python2 scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "d",
    ["/tools/ImpDump"],
)
def test_directories(host, d):
    """Test that appropriate directories were created."""
    directory = host.file(d)
    assert directory.exists
    assert directory.is_directory
    # Make sure that the directory is not empty
    assert host.run_expect([0], f'[ -n "$(ls --almost-all {d})" ]')


@pytest.mark.parametrize(
    "pkg",
    [
        "virtualenv",
    ],
)
def test_pip_packages(host, pkg):
    """Test that appropriate pip packages were installed."""
    assert pkg in host.pip.get_packages(pip_path="pip3")


@pytest.mark.parametrize(
    "d,pkgs",
    [
        ("/tools/ImpDump/.venv", ["impacket", "pycrypto"]),
    ],
)
def test_venvs(host, d, pkgs):
    """Test that appropriate Python virtualenvs were created."""
    directory = host.file(d)
    assert directory.exists
    assert directory.is_directory
    # Make sure that the virtualenv contains the expected packages
    installed_pkgs = host.pip.get_packages(pip_path=os.path.join(d, "bin", "pip"))
    for pkg in pkgs:
        assert pkg in installed_pkgs
