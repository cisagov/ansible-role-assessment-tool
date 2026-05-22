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
        # TODO - This test is currently allowed to fail for Ubuntu
        # Resolute, but that behavior should be reverted when possible.
        # See #84 for more details.
        pytest.param(
            "/tools/Auto-Egress-Assess",
            marks=pytest.mark.xfail(reason="Ubuntu Resolute cannot install this tool."),
        ),
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
        # TODO - This test is currently allowed to fail for Ubuntu
        # Resolute, but that behavior should be reverted when possible.
        # See #84 for more details.
        pytest.param(
            "pipenv",
            marks=pytest.mark.xfail(
                reason=(
                    "This package isn't installed on Ubuntu Resolute because "
                    "Auto-Egress-Assess is not installed there."
                )
            ),
        ),
        "virtualenv",
    ],
)
def test_packages(host, pkg):
    """Test that appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize(
    "d, pkgs",
    [
        # TODO - This test is currently allowed to fail for Ubuntu
        # Resolute, but that behavior should be reverted when possible.
        # See #84 for more details.
        pytest.param(
            "/tools/Auto-Egress-Assess/.venv",
            [
                # This package shows up with a different name in pip list
                # (bdist_mpkg versus bdist-mpkg) depending on the platform on
                # which it is installed, so we will skip testing for it.
                # "bdist_mpkg",
                "chardet",
                "dnslib",
                "impacket",
                # This package shows up with a different name in pip list
                # (importlib_metadata versus importlib-metadata) depending on
                # the platform on which it is installed, so we will skip
                # testing for it.
                # "importlib_metadata",
                "paramiko",
                "progress",
                "py2app",
                "pyftpdlib",
                "pyparsing",
                "python-dateutil",
                "pytz",
                "requests",
                "scapy",
            ],
            marks=pytest.mark.xfail(reason="Ubuntu Resolute cannot install this tool."),
        ),
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
def test_venvs(host, d, pkgs):
    """Test that appropriate Python virtualenvs were created."""
    directory = host.file(d)
    assert directory.exists
    assert directory.is_directory
    # Make sure that the virtualenv contains the expected packages
    installed_pkgs = host.pip.get_packages(pip_path=os.path.join(d, "bin", "pip"))
    for pkg in pkgs:
        assert pkg in installed_pkgs, f"Expected package {pkg} not installed in {d}."
