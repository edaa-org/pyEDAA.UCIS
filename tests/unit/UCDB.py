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
# Copyright 2021-2023 Electronic Design Automation Abstraction (EDA²)                                                  #
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
"""Testcase for UCDB file conversions."""
from pathlib      import Path
from unittest     import TestCase

from pyEDAA.UCIS.UCDB import Parser


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class ExportAndConvert(TestCase):
	def test_UCDB2Cobertura(self):
		ucdbPath = Path("data/ucdb.xml")
		coberturaPath = Path("data/cobertura.xml")

		parser = Parser(ucdbPath, False)
		model = parser.getCoberturaModel()

		coberturaContent = model.getXml()

		self.assertIsNotNone(coberturaContent)

		parser = Parser(ucdbPath, True)
		model = parser.getCoberturaModel()

		coberturaContent = model.getXml()

		self.assertIsNotNone(coberturaContent)


class CoverageValues(TestCase):
	def _parseUCDB(self, ucdbPath, mergeInstances):
		parser = Parser(ucdbPath, mergeInstances)
		model = parser.getCoberturaModel()
		model.getXml()

		return parser, model

	def test_multipleInstances(self):
		ucdbPath = Path("data/ucdb000_multiple_instances.xml")

		(parser, model) = self._parseUCDB(
			ucdbPath,
			False,
		)

		self.assertEqual(15, parser.statementsCount)
		self.assertEqual(14, parser.statementsCovered)
		self.assertEqual(7, model.linesValid)
		self.assertEqual(6, model.linesCovered)

		(parser, model) = self._parseUCDB(
			ucdbPath,
			True,
		)

		self.assertEqual(9, parser.statementsCount)
		self.assertEqual(8, parser.statementsCovered)
		self.assertEqual(7, model.linesValid)
		self.assertEqual(6, model.linesCovered)

	def test_allExcluded(self):
		ucdbPath = Path("data/ucdb001_all_excluded.xml")

		(parser, model) = self._parseUCDB(
			ucdbPath,
			False,
		)

		self.assertEqual(0, parser.statementsCount)
		self.assertEqual(0, parser.statementsCovered)
		self.assertEqual(0, model.linesValid)
		self.assertEqual(0, model.linesCovered)

		(parser, model) = self._parseUCDB(
			ucdbPath,
			True,
		)

		self.assertEqual(0, parser.statementsCount)
		self.assertEqual(0, parser.statementsCovered)
		self.assertEqual(0, model.linesValid)
		self.assertEqual(0, model.linesCovered)

	def test_partiallyExcluded(self):
		ucdbPath = Path("data/ucdb002_partially_excluded.xml")

		(parser, model) = self._parseUCDB(
			ucdbPath,
			False,
		)

		self.assertEqual(5, parser.statementsCount)
		self.assertEqual(4, parser.statementsCovered)
		self.assertEqual(5, model.linesValid)
		self.assertEqual(4, model.linesCovered)

		(parser, model) = self._parseUCDB(
			ucdbPath,
			True,
		)

		self.assertEqual(5, parser.statementsCount)
		self.assertEqual(4, parser.statementsCovered)
		self.assertEqual(5, model.linesValid)
		self.assertEqual(4, model.linesCovered)
