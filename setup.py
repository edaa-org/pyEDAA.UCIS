# ==================================================================================================================== #
#              _____ ____    _        _     _   _  ____ ___ ____                                                       #
#  _ __  _   _| ____|  _ \  / \      / \   | | | |/ ___|_ _/ ___|                                                      #
# | '_ \| | | |  _| | | | |/ _ \    / _ \  | | | | |    | |\___ \                                                      #
# | |_) | |_| | |___| |_| / ___ \  / ___ \ | |_| | |___ | | ___) |                                                     #
# | .__/ \__, |_____|____/_/   \_\/_/   \_(_)___/ \____|___|____/                                                      #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2021-2022 Patrick Lehmann - Bötzingen, Germany                                                             #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""Package installer for 'Tools to extract data from UCIS datafiles'."""
from pathlib             import Path
from pyTooling.Packaging import DescribePythonPackageHostedOnGitHub

gitHubNamespace =        "pyEDAA"
packageName =            "pyEDAA.UCIS"
packageDirectory =       packageName.replace(".", "/")
packageInformationFile = Path(f"{packageDirectory}/__init__.py")

DescribePythonPackageHostedOnGitHub(
	packageName=packageName,
	description="Tools to extract data from UCIS datafiles.",
	gitHubNamespace=gitHubNamespace,
	sourceFileWithVersion=packageInformationFile,
	developmentStatus="alpha",
	classifiers=[
		"Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
	],
	consoleScripts={
		"ucdb2cobertura": "pyEDAA.UCIS.CLI:main"
	}
)
