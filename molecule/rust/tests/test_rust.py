"""Module containing the tests for the rust scenario."""

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
        "/tools/rust-hello-cargo",
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
    "target",
    [
        "debug",
        "release",
    ],
)
def test_run_executables(host, target):
    """Test running the compiled executables."""
    cmd = host.run(f"/tools/rust-hello-cargo/target/{target}/hello_cargo")
    assert cmd.rc == 0, "hello_cargo command did not complete successfully"
    assert cmd.stdout == "Hello, world!\n"
