# Cargo build regression tests #

Run in a disposable Debian/Ubuntu environment with Ansible and the
`community.general` collection installed. The playbook installs the system Cargo
package, compiles a local dependency-free fixture with release, dev, test, bench
and custom profiles, and verifies repeat runs skip the existing binary.

```sh
ansible-playbook -i localhost, -c local tests/cargo.yml
```

For older Cargo versions without custom-profile support, test the built-in
profiles only:

```sh
ansible-playbook -i localhost, -c local tests/cargo.yml \
  -e '{"cargo_test_profiles": ["release", "dev"]}'
```
