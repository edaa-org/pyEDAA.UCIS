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
# Copyright 2021-2026 Electronic Design Automation Abstraction (EDA²)                                                  #
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
"""Testcase for CLI tests."""
import sys
from io            import StringIO
from re            import compile as re_compile
from typing        import Tuple
from unittest      import TestCase
from unittest.mock import patch

from pyEDAA.UCIS.CLI import Application, main


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


PROGRAM = "pyedaa-ucis"

class Testcase(TestCase):
	@staticmethod
	def _PrintToStdOutAndStdErr(out: StringIO, err: StringIO, stdoutEnd: str = "") -> Tuple[str, str]:
		out.seek(0)
		err.seek(0)

		stdout = out.read()
		stderr = err.read()

		print("-- STDOUT " + "-" * 70)
		print(stdout, end=stdoutEnd)
		if len(stderr) > 0:
			print("-- STDERR " + "-" * 70)
			print(stderr, end="")
		print("-" * 80)

		return stdout, stderr

	@staticmethod
	def _RemoveColorCodes(content: str) -> str:
		# WORKAROUND: removing color codes
		ansiEscape = re_compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		return ansiEscape.sub("", content)


class Help(Testcase):
	@patch("sys.argv", [])
	def test_NoOptions(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		app.Run()

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		self.assertIn("UCDB Service Program", stdout)
		self.assertIn(f"usage: {PROGRAM}", stdout)
		self.assertEqual("", stderr)

	@patch("sys.argv", ["help"])
	def test_HelpCommand(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		app.Run()

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		self.assertIn("UCDB Service Program", stdout)
		self.assertIn(f"usage: {PROGRAM}", stdout)
		self.assertEqual("", stderr)

	@patch("sys.argv", ["help", "expand"])
	def test_HelpForExport(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		app.Run()

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertIn("UCDB Service Program", stdout)
		# self.assertIn(f"usage: {PROGRAM}", stdout)
		# self.assertIn(f"usage: {PROGRAM}", stderr)
		self.assertEqual("", stderr)

	@patch("sys.argv", ["expand"])
	def test_UnknownCommand(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(2, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		self.assertIn(f"usage: {PROGRAM}", stdout)
		self.assertEqual("", stderr)

	@patch("sys.argv", ["help", "expand"])
	def test_HelpCommandUnknownCommand(self):
		print()

		sys.argv = [PROGRAM, "help", "expand"]

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		app.Run()

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		self.assertIn("Command expand is unknown.", stdout)
		self.assertEqual("", stderr)


class Version(Testcase):
	@patch("sys.argv", ["ucis", "version"])
	def test_VersionCommand(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		app.Run()

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		self.assertIn("UCDB Service Program", stdout)
		self.assertIn("Version:", stdout)
		self.assertEqual("", stderr)


class Export(Testcase):
	@patch("sys.argv", ["export"])
	def test_ExportCommandNoFilenames(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(2, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		self.assertIn("UCDB Service Program", stdout)
		self.assertEqual("", stderr)

	@patch("sys.argv", ["export", "--ucdb", "file1.xml", "--cobertura", "file2.xml"])
	def test_ExportCommandWithFilenames(self):
		print()

		app = Application()
		app._stdout, app._stderr = out, err = StringIO(), StringIO()
		try:
			app.Run()
		except SystemExit as ex:
			self.assertEqual(2, ex.code)

		stdout, stderr = self._PrintToStdOutAndStdErr(out, err)

		# self.assertIn("UCDB Service Program", stdout)
		# self.assertIn("ERROR", stdout)
		self.assertEqual("", stderr)
