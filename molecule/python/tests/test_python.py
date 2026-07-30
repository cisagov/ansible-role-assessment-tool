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
        # This tool can no longer be installed on Bullseye because it
        # pins mysql-connector-python to version 9.5.0, which requires
        # Python 3.10 or later.  Bullseye only provides Python 3.9.
        #
        # TODO - Revert this change.  See #78 for more details.
        # "/tools/dirsearch",
        "/tools/mitm6",
        "/tools/sqlmap",
        "/tools/sshenum",
    ],
)
def test_directories(host, d, request):
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
def test_packages(host, pkg, request):
    """Test that appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize(
    "d, pkgs",
    [
        # This tool can no longer be installed on Bullseye because it
        # pins mysql-connector-python to version 9.5.0, which requires
        # Python 3.10 or later.  Bullseye only provides Python 3.9.
        #
        # TODO - Revert this change.  See #78 for more details.
        # (
        #     "/tools/dirsearch/.venv",
        #     [
        #         "certifi",
        #         "cffi",
        #         "cryptography",
        #         "urllib3",
        #     ],
        # ),
        ("/tools/mitm6/.venv", ["mitm6"]),
        # There is no venv for sqlmap since it has no dependencies.
        # ("/tools/sqlmap/.venv", []),
        ("/tools/sshenum/.venv", ["paramiko"]),
    ],
)
def test_venvs(host, d, pkgs, request):
    """Test that appropriate Python virtualenvs were created."""
    directory = host.file(d)

    assert directory.exists
    assert directory.is_directory
    # Make sure that the virtualenv contains the expected packages
    installed_pkgs = host.pip.get_packages(pip_path=os.path.join(d, "bin", "pip"))
    for pkg in pkgs:
        assert pkg in installed_pkgs, f"Expected package {pkg} not installed in {d}."
