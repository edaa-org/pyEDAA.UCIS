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
"""Testcase for CLI tests."""
import sys
from io            import StringIO
from unittest      import TestCase
from unittest.mock import patch

from pyEDAA.UCIS.CLI import Program, main


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


PROGRAM = "pyedaa-ucis"

class Help(TestCase):
	_program: Program

	def setUp(self) -> None:
		self._program = Program()

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_NoOptions(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM]

		self._program.Run()

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("UCDB Service Program", stdout)
		self.assertIn(f"usage: {PROGRAM}", stdout)
		self.assertEqual("", stderr)

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_HelpCommand(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "help"]

		self._program.Run()

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("UCDB Service Program", stdout)
		self.assertIn(f"usage: {PROGRAM}", stdout)
		self.assertEqual("", stderr)

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_HelpForExport(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "help", "export"]

		self._program.Run()

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("UCDB Service Program", stdout)
		self.assertIn(f"usage: {PROGRAM}", stdout)
		self.assertEqual("", stderr)

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_UnknownCommand(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "expand"]

		with self.assertRaises(SystemExit) as ex:
			self._program.Run()

		self.assertEqual(2, ex.exception.code)

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertEqual("", stdout)
		self.assertIn(f"usage: {PROGRAM}", stderr)

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_HelpCommandUnknownCommand(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "help", "expand"]

		self._program.Run()

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("Command expand is unknown.", stdout)
		self.assertEqual("", stderr)


class Version(TestCase):
	_program: Program

	def setUp(self) -> None:
		self._program = Program()

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_VersionCommand(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "version"]

		self._program.Run()

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("UCDB Service Program", stdout)
		self.assertIn("Version:", stdout)
		self.assertEqual("", stderr)


class Export(TestCase):
	_program: Program

	def setUp(self) -> None:
		self._program = Program()

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_ExportCommandNoFilenames(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "export"]

		with self.assertRaises(SystemExit) as ex:
			self._program.Run()

		self.assertEqual(3, ex.exception.code)

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("UCDB Service Program", stdout)
		self.assertEqual("", stderr)

	@patch('sys.stderr', new_callable=StringIO)
	@patch('sys.stdout', new_callable=StringIO)
	def test_ExportCommandWithFilenames(self, stdoutStream: StringIO, stderrStream: StringIO):
		sys.argv = [PROGRAM, "export", "--ucdb", "file1.xml", "--cobertura", "file2.xml"]

		with self.assertRaises(SystemExit) as ex:
			main()

		self.assertEqual(1, ex.exception.code)

		stdout = stdoutStream.getvalue()
		stderr = stderrStream.getvalue()
		self.assertIn("UCDB Service Program", stdout)
		self.assertIn("ERROR", stdout)
		self.assertEqual("", stderr)
