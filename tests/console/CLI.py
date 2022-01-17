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
# Copyright 2021-2022 Electronic Design Automation Abstraction (EDA²)                                                  #
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
"""Testcase for pyEDAA.UCIS service program."""
import shutil
import subprocess
from unittest     import TestCase


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Help(TestCase):
	PROGRAM_NAME = "pyedaa-ucis"

	def test_Installation(self):
		prog = shutil.which(self.PROGRAM_NAME)

		self.assertIsNotNone(prog)
		self.assertTrue(prog.endswith(self.PROGRAM_NAME))

	def test_NoOptions(self):
		completion = subprocess.run(["pyedaa-ucis"], capture_output=True)

		stdout = completion.stdout.decode("utf-8")

		self.assertEqual(0, completion.returncode)
		self.assertIn("UCDB Service Program", stdout)
