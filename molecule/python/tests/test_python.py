"""Module containing the tests for the python scenario."""

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
    [
        "/tools/dirsearch",
        "/tools/mitm6",
        "/tools/sqlmap",
        "/tools/sshenum",
    ],
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
def test_packages(host, pkg):
    """Test that appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize(
    "d,pkgs",
    [
        ("/tools/sshenum/.venv", ["paramiko"]),
        (
            "/tools/dirsearch/.venv",
            ["certifi", "urllib3", "cryptography", "cffi", "MarkupSafe"],
        ),
        ("/tools/mitm6/.venv", ["mitm6"]),
        # There is no venv for sqlmap since it has no dependencies.
        # ("/tools/sqlmap/.venv", []),
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
