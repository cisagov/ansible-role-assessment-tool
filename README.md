# ansible-role-assessment-tool #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-assessment-tool/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-assessment-tool/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-assessment-tool/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-assessment-tool/actions/workflows/codeql-analysis.yml)

This Ansible role is used to install assessment tools to Debian,
Ubuntu, or Kali Linux.  This role can also be configured to provide
some language-specific extras:

- C# - The `assessment_tool_csharp` role variable can be set to `true`
  to install the [Mono Project](https://www.mono-project.com/) tools
  for C# development on Linux.
- Go - The `assessment_tool_go` role variable can be set to `true` to
  install the [Go](https://go.dev/) development tools.
- PowerShell - The `assessment_tool_powershell` role variable can be
  set to `true` to install
  [PowerShell](https://en.wikipedia.org/wiki/PowerShell).
- Python - The `assessment_tool_python` role variable can be set to
  `true` and used in conjunction with the role variables
  `assessment_tool_pip_packages` or
  `assessment_tool_pip_requirements_file` to install a [Python virtual
  environment](https://docs.python.org/3/glossary.html#term-virtual-environment)
  with the tool's dependencies pre-installed.  To activate the virtual
  environment, simply use the command `source
  /path/to/tool/.venv/bin/activate`.  When you are done using the
  tool, simply `deactivate`.
- Rust - The `assessment_tool_rust` role variable can be set to `true`
  and used in conjunction with the role variable
  `assessment_tool_cargo_packages` to install `assessment_tool_cargo`
  and the desired packages.

## Nota Bene ##

By default, when using `vars:` within the `roles:` section of a
playbook, the variables are added to the play variables.  This is
normally not a problem, but it definitely can be if you are running
the same role more than once with a different set of vars.
Fortunately, Ansible provides the configuration setting
`private_role_vars` to allow enabling of private role variables.  If
you use this role more than once in a playbook, then you will want to
set `private_role_vars` to `true`.

For more details, see [this
link](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#using-roles-at-the-play-level)
and [this
link](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-private-role-vars).

As an alternative, you might also consider using the
[`ansible.builtin.include_role`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html)
and/or
[`ansible.builtin.import_role`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html)
Ansible modules instead of including roles via the `roles:` section of
the playbook.  Including Ansible roles using these modules does not
result in their variables being added to the play variables and
therefore avoids this issue altogether.

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| assessment_tool_archive_src | A URL or a file path on the remote host pointing to an archive (tar or zip) containing the tool.  If left undefined then no archive will be installed, but the install directory will still be created and language-specific tooling will still be installed. | n/a | No |
| assessment_tool_cargo_build | A Boolean indicating whether or not the Rust tool should be built using `cargo`; if so then we will run `cargo build` from the project's root directory. | `true` | No |
| assessment_tool_cargo_install_dir | The directory where the `cargo` packages should be installed.  Only read if  `assessment_tool_cargo_packages` is present. | `install_dir` | No |
| assessment_tool_cargo_packages | A list of `cargo` packages to install. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| assessment_tool_cargo_profile | The `cargo` profile to use when building the project. | `release` | No |
| assessment_tool_csharp | A Boolean indicating whether or not the tool is written in C#; if it is then we will install the mono C# toolchain. | `false` | No |
| assessment_tool_go | A Boolean indicating whether or not the tool is written in Go; if it is then we will install the Go development toolchain. | `false` | No |
| assessment_tool_go_build | A Boolean indicating whether or not the Go tool should be built; if so then we will run `go build` from the project's root directory. | `true` | No |
| assessment_tool_group | The group that will own the directory where this tool is installed. | `root` | No |
| assessment_tool_install_dir | The directory on the remote host where the tool should be installed. | n/a | Yes |
| assessment_tool_mode | The mode to assign the directory where this tool is installed. | `0775` | No |
| assessment_tool_owner | The user that will own the directory where this tool is installed. | `root` | No |
| assessment_tool_pip_extra_args | Extra arguments to give to `pip` when installing packages into the Python virtualenv. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| assessment_tool_pip_packages | A list of `pip` packages to install into the Python virtualenv. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| assessment_tool_pip_requirements_file | The path to a `pip` requirements file listing dependencies to install into the Python virtualenv. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| assessment_tool_powershell | A Boolean indicating whether or not the tool is written in PowerShell; if it is then we will install the powershell system package. | `false` | No |
| assessment_tool_python | A Boolean that *can* indicate that Python is to be installed.  If either assessment_tool_pip_packages or assessment_tool_pip_requirements_file is defined, or if either assessment_tool_python2 or assessmemt_tool_python_install_development_dependencies is `true`, then Python will be installed anyway and a Python virtual environment created, but this variable is occasionally useful, e.g., when installing a tool that lacks any Python packaging and has no dependencies. | `false` | No |
| assessment_tool_python2 | A Boolean indicating whether or not the tool is strictly for Python 2; if it is then we will install the system package that provides the Python 2 interpreter.  If assessment_tool_pip_requirements_file or assessment_tool_pip_packages are defined then we will also create a Python 2 virtual environment.  Note that Debian no longer supports Python 2 as of Bookworm. | `false` | No |
| assessment_tool_python_install_development_dependencies | A Boolean indicating whether or not Python development dependencies are to be installed.  These dependencies are useful, e.g., if pip must build a wheel. | `false` | No |
| assessment_tool_rust | A Boolean indicating whether or not the tool is written in Rust; if it is then we will install the system packages that provide `cargo`. | `false` | No |
| assessment_tool_unarchive_extra_opts | A list of extra options to be passed to the ansible.builtin.unarchive Ansible module.  When installing a tarball from a GitHub repository, for example, it is often useful to set this value to "[--strip-components=1]". | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| assessment_tool_virtualenv_dir | The directory where the Python virtualenv should be created.  Only read if at least one of `assessment_tool_pip_packages` or `assessment_tool_pip_requirements_file` is present. | `install_dir/.venv` | No |

## Dependencies ##

- [cisagov/ansible-role-backports](https://github.com/cisagov/ansible-role-backports):
  On Debian Buster we need a newer version of the `golang` package in order to
  build Go-based projects.
- [cisagov/ansible-role-pip](https://github.com/cisagov/ansible-role-pip):
  Pip is required to create a virtual environment for Python-based projects.
- [cisagov/ansible-role-python](https://github.com/cisagov/ansible-role-python):
  Python is required to create a virtual environment for Python-based projects.

## Example Playbook ##

### Installing a C# Tool ###

Here's how to use it in a playbook to install a C# tool:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install Internal-Monologue
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/eladshamir/Internal-Monologue/tarball/master
        assessment_tool_install_dir: /tools/Internal-Monologue
        assessment_tool_csharp: true
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

### Installing a Go Tool ###

Here's how to use it in a playbook to install a Go tool:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install ScareCrow
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/optiv/ScareCrow/tarball/main
        assessment_tool_install_dir: /tools/ScareCrow
        assessment_tool_go: true
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

### Installing a PowerShell Tool ###

Here's how to use it in a playbook to install a PowerShell tool:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install PowerUpSQL
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/NetSPI/PowerUpSQL/tarball/master
        assessment_tool_install_dir: /tools/PowerUpSQL
        assessment_tool_powershell: true
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

### Installing a Python Tool ###

#### With Dependencies Listed in a `requirements.txt` File ####

Here's how to use it in a playbook to install a Python tool using a
`requirements.txt` file:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install dirsearch
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/maurosoria/dirsearch/tarball/master
        assessment_tool_install_dir: /tools/dirsearch
        assessment_tool_pip_requirements_file: requirements.txt
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

#### With Dependencies Listed in a `setup.py` File ####

Here's how to use it in a playbook to install a Python tool using a
`setup.py` file:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install Hasher
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/FortyNorthSecurity/Hasher/tarball/master
        assessment_tool_install_dir: /tools/Hasher
        assessment_tool_pip_packages:
          - '.'
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

#### Using a List of `pip` Packages ####

Here's how to use it in a playbook to install a Python tool using a
list of `pip` packages:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install sshenum
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/MacR6/sshenum/tarball/master
        assessment_tool_install_dir: /tools/sshenum
        assessment_tool_pip_packages:
          - paramiko
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

#### Simply Creating a Virtual Environment ####

Here's how to use it in a playbook to simply create a Python virtual
environment:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install mitm6
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_install_dir: /tools/mitm6
        assessment_tool_pip_packages:
          - mitm6
```

### Installing a Rust Tool ###

Here's how to use it in a playbook to install a tool that requires a
Rust compiler:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install CrackMapExec
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/Porchetta-Industries/CrackMapExec/tarball/master
        assessment_tool_install_dir: /tools/CrackMapExec
        assessment_tool_rust: true
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

### Installing a Tool That Is Not Based on C#, PowerShell, Python, or Rust ###

Here's how to use it in a playbook to install a generic (C-based, in
this case) tool:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install datapipe
      ansible.builtin.include_role:
        name: assessment_tool
      vars:
        assessment_tool_archive_src: https://github.com/bovine/datapipe/tarball/master
        assessment_tool_install_dir: /tools/datapipe
        assessment_tool_unarchive_extra_opts:
          - --strip-components=1
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Shane Frasier - <jeremy.frasier@gwe.cisa.dhs.gov>
