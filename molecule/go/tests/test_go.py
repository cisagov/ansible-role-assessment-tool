"""Module containing the tests for the go scenario."""

# Standard Python Libraries
import os
import stat

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "d",
    [
        "/tools/ScareCrow",
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
        "git",
        "golang",
    ],
)
def test_packages(host, pkg):
    """Test that appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize(
    "f",
    [
        "/tools/ScareCrow/ScareCrow",
    ],
)
def test_build_products(host, f):
    """Test that appropriate build products were created."""
    ff = host.file(f)
    assert ff.exists
    assert ff.is_file
    assert ff.mode & stat.S_IXUSR == stat.S_IXUSR
