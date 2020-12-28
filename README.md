# ansible-role-assessment-tool #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-assessment-tool/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-assessment-tool/actions)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/ansible-role-assessment-tool.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-assessment-tool/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/ansible-role-assessment-tool.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-assessment-tool/context:python)

This Ansible role is used to install assessment tools to Kali Linux
from a URL pointing to an archive (tar or zip) containing the tool.
This role can also be configured to provide some language-specific
extras:

* C# - The `csharp` role variable can be set to `yes` to install the
  [Mono Project](https://www.mono-project.com/) tools for C#
  development on Linux.
* PowerShell - The `powershell` role variable can be set to `yes` to
  install [PowerShell](https://en.wikipedia.org/wiki/PowerShell).
* Python - The `python` role variable can be set to `yes` and used in
  conjunction with the role variables `pip_packages` or
  `pip_requirements_file` to install a [Python virtual
  environment](https://docs.python.org/3/glossary.html#term-virtual-environment)
  with the tool's dependencies pre-installed.  To activate the virtual
  environment, simply use the command `source
  /path/to/tool/.venv/bin/activate`.  When you are done using the
  tool, simply `deactivate`.

## Requirements ##

None.

## Role Variables ##

* `archive_url` - a URL pointing to an archive (tar or zip) containing
  the tool.  Required.
* `csharp` - a Boolean indicating whether or not the tool is written
  in C#; if it is then we will install the mono C# toolchain.
  Defaults to false.
* `group` - the group that will own the directory where this tool is
  installed.  Defaults to "root".
* `install_dir` - the directory on the remote host where the tool
  should be installed.  Required.
* `mode` - the mode to assign the directory where this tool is
  installed.  Defaults to 0775.
* `pip_packages` - a list of pip packages to install into the Python
  virtualenv.  Only read if python is true.
* `pip_requirements_file` - path to a pip requirements file listing
  dependencies to install into the Python virtualenv.  Only read if
  python is true.
* `powershell` - a Boolean indicating whether or not the tool is
  written in PowerShell; if it is then we will install the powershell
  system package.  Defaults to false.
* `python` - a Boolean indicating whether or not the tool is
  Python-based; if it is then a Python virtualenv will be created for
  the tool.  Defaults to false.
* `virtualenv_dir` - the directory where the Python virtualenv should
  be created.  Defaults to install_dir/.venv.  Only read if python is
  true.

## Dependencies ##

None.

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
        archive_url: https://github.com/eladshamir/Internal-Monologue/tarball/master/
        install_dir: /tools/Internal-Monologue
        csharp: yes
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
        archive_url: https://github.com/NetSPI/PowerUpSQL/tarball/master
        install_dir: /tools/PowerUpSQL
        powershell: yes
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
        archive_url: https://github.com/maurosoria/dirsearch/tarball/master
        install_dir: /tools/dirsearch
        pip_requirements_file: requirements.txt
        python: yes
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
        archive_url: https://github.com/FortyNorthSecurity/Hasher/tarball/master
        install_dir: /tools/Hasher
        pip_packages:
          - '.'
        python: yes
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
        archive_url: https://github.com/MacR6/sshenum/tarball/master
        install_dir: /tools/sshenum
        pip_packages:
          - paramiko
        python: yes
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
        archive_url: https://github.com/bovine/datapipe/tarball/master
        install_dir: /tools/datapipe
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
