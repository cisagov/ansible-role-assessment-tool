"""Module containing the tests for the rust scenario."""

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
        "/tools/ripgen",
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
        "cargo",
    ],
)
def test_packages(host, pkg):
    """Test that appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize(
    "path",
    [
        "/tools/ripgen/target/release/ripgen",
    ],
)
def test_build_product(host, path):
    """Test that the build product exists."""
    product = host.file(path)
    assert product.exists
    assert product.is_file
    assert product.mode | stat.S_IXUSR
