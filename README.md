# ansible-role-assessment-tool #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-assessment-tool/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-assessment-tool/actions)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/ansible-role-assessment-tool.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-assessment-tool/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/ansible-role-assessment-tool.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-assessment-tool/context:python)

This Ansible role is used to install assessment tools to Kali Linux
from a URL pointing to an archive (tar or zip) containing the tool.

## Requirements ##

None.

## Role Variables ##

* archive_url - a URL pointing to an archive (tar or zip) containing
  the tool
* csharp - a Boolean indicating whether or not the tool is written in
  C#; if it is then we will install the mono C# toolchain.  Defaults
  to false.
* group - the group that will own the directory where this tool is
  installed.  Defaults to "root".
* install_dir - the directory on the remote host where the tool should
  be installed

## Dependencies ##

None.

## Example Playbook ##

Here's how to use it in a playbook:

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
