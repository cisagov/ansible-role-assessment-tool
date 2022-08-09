# ansible-role-assessment-tool #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-assessment-tool/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-assessment-tool/actions)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/ansible-role-assessment-tool.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-assessment-tool/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/ansible-role-assessment-tool.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-assessment-tool/context:python)

This Ansible role is used to install assessment tools to Debian,
Ubuntu, or Kali Linux.  This role can also be configured to provide
some language-specific extras:

- C# - The `csharp` role variable can be set to `yes` to install the
  [Mono Project](https://www.mono-project.com/) tools for C#
  development on Linux.
- Go - The `go` role variable can be set to `yes` to install the
  [Go](https://go.dev/) development tools.
- PowerShell - The `powershell` role variable can be set to `yes` to
  install [PowerShell](https://en.wikipedia.org/wiki/PowerShell).
- Python - The `python` role variable can be set to `yes` and used in
  conjunction with the role variables `pip_packages` or
  `pip_requirements_file` to install a [Python virtual
  environment](https://docs.python.org/3/glossary.html#term-virtual-environment)
  with the tool's dependencies pre-installed.  To activate the virtual
  environment, simply use the command `source
  /path/to/tool/.venv/bin/activate`.  When you are done using the
  tool, simply `deactivate`.

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

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| archive_src | A URL or a file path on the remote host pointing to an archive (tar or zip) containing the tool.  If left undefined then no archive will be installed, but the install directory will still be created and language-specific tooling will still be installed. | n/a | No |
| csharp | A Boolean indicating whether or not the tool is written in C#; if it is then we will install the mono C# toolchain. | `false` | No |
| go | A Boolean indicating whether or not the tool is written in Go; if it is then we will install the Go development toolchain. | `false` | No |
| go_build | A Boolean indicating whether or not the Go tool should be built; if so then we will run `go build` from the project's root directory. | `true` | No |
| group | The group that will own the directory where this tool is installed. | `root` | No |
| install_dir | The directory on the remote host where the tool should be installed. | n/a | Yes |
| mode | The mode to assign the directory where this tool is installed. | `0775` | No |
| owner | The user that will own the directory where this tool is installed. | `root` | No |
| pip_extra_args | A extra arguments to give to pip when installing packages into the Python virtualenv. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| pip_packages | A list of pip packages to install into the Python virtualenv. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| pip_requirements_file | The path to a pip requirements file listing dependencies to install into the Python virtualenv. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| powershell | A Boolean indicating whether or not the tool is written in PowerShell; if it is then we will install the powershell system package. | `false` | No |
| python2 | A Boolean indicating whether or not the tool is strictly for Python 2; if it is then we will install the system package that provides the Python 2 interpreter and will create a Python 2 virtual environment. | `false` | No |
| unarchive_extra_opts | A list of extra options to be passed to the ansible.builtin.unarchive Ansible module.  When installing a tarball from a GitHub repository, for example, it is often useful to set this value to "[--strip-components=1]". | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| virtualenv_dir | The directory where the Python virtualenv should be created.  Only read if at least one of `pip_packages` or `pip_requirements_file` is present. | `install_dir/.venv` | No |

## Dependencies ##

- [cisagov/ansible-role-backports](https://github.com/cisagov/ansible-role-backports):
  On Debian Buster we need a newer version of the `golang` package in order to
  build Go-based projects.

## Example Playbook ##

### Installing a C# Tool ###

Here's how to use it in a playbook to install a C# tool:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/eladshamir/Internal-Monologue/tarball/master
        install_dir: /tools/Internal-Monologue
        csharp: yes
        unarchive_extra_opts:
          - --strip-components=1
```

### Installing a Go Tool ###

Here's how to use it in a playbook to install a Go tool:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/optiv/ScareCrow/tarball/main
        install_dir: /tools/ScareCrow
        go: yes
        unarchive_extra_opts:
          - --strip-components=1
```

### Installing a PowerShell Tool ###

Here's how to use it in a playbook to install a PowerShell tool:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/NetSPI/PowerUpSQL/tarball/master
        install_dir: /tools/PowerUpSQL
        powershell: yes
        unarchive_extra_opts:
          - --strip-components=1
```

### Installing a Python Tool ###

#### With Dependencies Listed in a `requirements.txt` File ####

Here's how to use it in a playbook to install a Python tool using a
`requirements.txt` file:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/maurosoria/dirsearch/tarball/master
        install_dir: /tools/dirsearch
        pip_requirements_file: requirements.txt
        unarchive_extra_opts:
          - --strip-components=1
```

#### With Dependencies Listed in a `setup.py` File ####

Here's how to use it in a playbook to install a Python tool using a
`setup.py` file:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/FortyNorthSecurity/Hasher/tarball/master
        install_dir: /tools/Hasher
        pip_packages:
          - '.'
        unarchive_extra_opts:
          - --strip-components=1
```

#### Using a List of `pip` Packages ####

Here's how to use it in a playbook to install a Python tool using a
list of `pip` packages:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/MacR6/sshenum/tarball/master
        install_dir: /tools/sshenum
        pip_packages:
          - paramiko
        unarchive_extra_opts:
          - --strip-components=1
```

#### Simply Creating a Virtual Environment ####

Here's how to use it in a playbook to simply create a virtual
environment:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        install_dir: /tools/mitm6
        pip_packages:
          - mitm6
```

### Installing a Tool That Is Not Based on C#, PowerShell, or Python ###

Here's how to use it in a playbook to install a generic (C-based, in
this case) tool:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - role: assessment_tool
      vars:
        archive_src: https://github.com/bovine/datapipe/tarball/master
        install_dir: /tools/datapipe
        unarchive_extra_opts:
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

Shane Frasier - <jeremy.frasier@trio.dhs.gov>
