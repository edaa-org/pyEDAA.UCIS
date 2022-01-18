<p align="center">
  <a title="edaa-org.github.io/pyEDAA.UCIS" href="https://edaa-org.github.io/pyEDAA.UCIS"><img height="80px" src="doc/_static/logo.svg"/></a>
</p>

[![Sourcecode on GitHub](https://img.shields.io/badge/pyEDAA-UCIS-29b6f6.svg?longCache=true&style=flat-square&logo=GitHub&labelColor=0277bd)](https://GitHub.com/edaa-org/pyEDAA.UCIS)
[![Sourcecode License](https://img.shields.io/pypi/l/pyEDAA.UCIS?longCache=true&style=flat-square&logo=Apache&label=code)](LICENSE.md)
[![Documentation](https://img.shields.io/website?longCache=true&style=flat-square&label=edaa-org.github.io%2FpyEDAA.UCIS&logo=GitHub&logoColor=fff&up_color=blueviolet&up_message=Read%20now%20%E2%9E%9A&url=https%3A%2F%2Fedaa-org.github.io%2FpyEDAA.UCIS%2Findex.html)](https://edaa-org.github.io/pyEDAA.UCIS/)
[![Documentation License](https://img.shields.io/badge/doc-CC--BY%204.0-green?longCache=true&style=flat-square&logo=CreativeCommons&logoColor=fff)](LICENSE.md)
[![Gitter](https://img.shields.io/badge/chat-on%20gitter-4db797.svg?longCache=true&style=flat-square&logo=gitter&logoColor=e8ecef)](https://gitter.im/hdl/community)  
[![PyPI](https://img.shields.io/pypi/v/pyEDAA.UCIS?longCache=true&style=flat-square&logo=PyPI&logoColor=FBE072)](https://pypi.org/project/pyEDAA.UCIS/)
![PyPI - Status](https://img.shields.io/pypi/status/pyEDAA.UCIS?longCache=true&style=flat-square&logo=PyPI&logoColor=FBE072)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyEDAA.UCIS?longCache=true&style=flat-square&logo=PyPI&logoColor=FBE072)  
[![GitHub Workflow - Build and Test Status](https://img.shields.io/github/workflow/status/edaa-org/pyEDAA.UCIS/Pipeline/main?longCache=true&style=flat-square&label=Build%20and%20Test&logo=GitHub%20Actions&logoColor=FFFFFF)](https://GitHub.com/edaa-org/pyEDAA.UCIS/actions/workflows/Pipeline.yml)
[![Libraries.io status for latest release](https://img.shields.io/librariesio/release/pypi/pyEDAA.UCIS?longCache=true&style=flat-square&logo=Libraries.io&logoColor=fff)](https://libraries.io/github/edaa-org/pyEDAA.UCIS)
[![Codacy - Quality](https://img.shields.io/codacy/grade/63bd2bd65585447a9f6d7ad4e7d82a35?longCache=true&style=flat-square&logo=Codacy)](https://app.codacy.com/gh/edaa-org/pyEDAA.UCIS)
[![Codacy - Coverage](https://img.shields.io/codacy/coverage/63bd2bd65585447a9f6d7ad4e7d82a35?longCache=true&style=flat-square&logo=Codacy)](https://app.codacy.com/gh/edaa-org/pyEDAA.UCIS)
[![Codecov - Branch Coverage](https://img.shields.io/codecov/c/github/edaa-org/pyEDAA.UCIS?longCache=true&style=flat-square&logo=Codecov)](https://codecov.io/gh/edaa-org/pyEDAA.UCIS)

<!--
[![Dependent repos (via libraries.io)](https://img.shields.io/librariesio/dependent-repos/pypi/pyEDAA.UCIS?longCache=true&style=flat-square&logo=GitHub)](https://GitHub.com/edaa-org/pyEDAA.UCIS/network/dependents)
[![Requires.io](https://img.shields.io/requires/github/edaa-org/pyEDAA.UCIS?longCache=true&style=flat-square)](https://requires.io/github/EDAA-ORG/pyEDAA.UCIS/requirements/?branch=main)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/pyEDAA.UCIS?longCache=true&style=flat-square)](https://libraries.io/github/edaa-org/pyEDAA.UCIS/sourcerank)
-->

Unified Coverage Interoperability Standard (UCIS)

<p align="center">
  <a title="edaa-org.github.io/pyEDAA.UCIS" href="https://edaa-org.github.io/pyEDAA.UCIS"><img height="275px" src="doc/_static/work-in-progress.png"/></a>
</p>

## Main Goals

* Parse UCDB files and provide a UCDB data model.
* Export and convert data from UCDB to Cobertura format.
* Also support flavors not following the Unified Coverage Interoperability Standard (UCIS).

## Use Cases
 
* Collect and merge code coverage with Active-HDL / Riviera-PRO and convert via UCDB format to Cobertura files, so code coverage can be published to e.g. GitLab, Codacy or CodeCov.


## Usage

```Bash
# Convert ACDB file into UCDB file (XML format)
acdb2xml -i aggregate.acdb -o ucdb.xml

# Convert UCDB file into Cobertura format
pyedaa-ucis export --ucdb ucdb.xml --cobertura cobertura.xml
```


# References

- [accellera.org/activities/working-groups/ucis](https://www.accellera.org/activities/working-groups/ucis/)
- [accellera.org/downloads/standards/ucis](https://www.accellera.org/downloads/standards/ucis)
- [fvutils/pyucis](https://github.com/fvutils/pyucis)
  - [fvutils/pyucis-viewer](https://github.com/fvutils/pyucis-viewer)
- [UCIS licensing [umarcor/umarcor#3]](https://github.com/umarcor/umarcor/issues/3)


## Contributors
* [Patrick Lehmann](https://github.com/Paebbels) (Maintainer)
* [Unai Martinez-Corral](https://GitHub.com/umarcor) (Maintainer)
* [Artur Porebski (Aldec Inc.)](https://github.com/por3bski)
* [Michal Pacula (Aldec Inc.)](https://github.com/mikep996)
* [and more...](https://github.com/edaa-org/pyEDAA.UCIS/graphs/contributors)


## License

This Python package (source code) licensed under [Apache License 2.0](LICENSE.md).  
The accompanying documentation is licensed under [Creative Commons - Attribution 4.0 (CC-BY 4.0)](doc/Doc-License.rst).

-------------------------
SPDX-License-Identifier: Apache-2.0
