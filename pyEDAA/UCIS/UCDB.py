# ==================================================================================================================== #
#               _____ ____    _        _     _   _  ____ ___ ____                                                      #
#   _ __  _   _| ____|  _ \  / \      / \   | | | |/ ___|_ _/ ___|                                                     #
#  | '_ \| | | |  _| | | | |/ _ \    / _ \  | | | | |    | |\___ \                                                     #
#  | |_) | |_| | |___| |_| / ___ \  / ___ \ | |_| | |___ | | ___) |                                                    #
#  | .__/ \__, |_____|____/_/   \_\/_/   \_(_)___/ \____|___|____/                                                     #
#  |_|    |___/                                                                                                        #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Artur Porebski (Aldec Inc.)                                                                                        #
#   Michal Pacula  (Aldec Inc.)                                                                                        #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2021-2022 Electronic Design Automation Abstraction (EDA²)                                                  #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#          http://www.apache.org/licenses/LICENSE-2.0                                                                  #
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
"""Data model of the UCDB format."""
from collections import namedtuple, defaultdict
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from typing import List, Tuple, Dict, DefaultDict

from lxml import etree
from pyTooling.Decorators import export

from pyEDAA.UCIS.Cobertura import Class, Coverage, Package


UCDB_EXCLUDE_PRAGMA = 0x00000020
UCDB_EXCLUDE_FILE = 0x00000040
UCDB_EXCLUDE_INST = 0x00000080
UCDB_EXCLUDE_AUTO = 0x00000100

UCDB_EXCLUDED = (
	UCDB_EXCLUDE_FILE | UCDB_EXCLUDE_PRAGMA | UCDB_EXCLUDE_INST | UCDB_EXCLUDE_AUTO
)

StatementData = namedtuple(
	"StatementData",
	["file", "line", "index", "instance", "hits"],
)


@export
class UcdbParserException(Exception):
	"""Base-class for other UCDB Parser exceptions"""


@export
class InternalErrorOccurred(UcdbParserException):
	"""Raised when internal error occurred"""


@export
class Parser:
	_mergeInstances: bool
	_tree: etree._ElementTree
	_nsmap: Dict
	_coverage: Coverage
	statementsCount: int
	statementsCovered: int

	def __init__(self, ucdbFile: Path, mergeInstances: bool):
		self._mergeInstances = mergeInstances

		with ucdbFile.open("r") as filename:
			self._tree = etree.parse(filename)

		self._nsmap = {
			k: v for (k, v) in self._tree.getroot().nsmap.items() if k is not None
		}

		self._coverage = Coverage()

		self.statementsCount = 0
		self.statementsCovered = 0

	def getCoberturaModel(self) -> Coverage:
		self._parseStatementCoverage()

		return self._coverage

	def _groupByIndex(self, statements: List[StatementData]) -> List[StatementData]:
		groupedStmts = []

		sortedStmts = sorted(statements, key=attrgetter("index"))
		for index, stmts in groupby(sortedStmts, key=attrgetter("index")):
			hit = any((stmt.hits for stmt in stmts))

			groupedStmts.append(
				StatementData(
					file=statements[0].file,
					line=statements[0].line,
					index=index,
					instance="",
					hits=hit,
				)
			)

		return groupedStmts

	def _parseStatementCoverage(self) -> None:
		scopes = self._tree.xpath(
			"/ux:ucdb/ux:scope[.//ux:bin[@type='STMTBIN']]", namespaces=self._nsmap
		)

		if not isinstance(scopes, list):
			raise InternalErrorOccurred(f"Unexpected type: '{scopes.__class__.__name__}'.")

		nodes: List[etree._Element] = []

		for scopeNode in scopes:
			if not isinstance(scopeNode, etree._Element):
				raise InternalErrorOccurred(f"Unexpected type: '{scopeNode.__class__.__name__}'.")

			typeName = scopeNode.get("type")

			if typeName is None:
				raise InternalErrorOccurred("Unexpected 'None' value.")

			if typeName.startswith("DU_"):
				continue

			statementBins = scopeNode.xpath(".//ux:bin[@type='STMTBIN']", namespaces=self._nsmap)

			if not isinstance(statementBins, list):
				raise InternalErrorOccurred(f"Unexpected type: '{statementBins.__class__.__name__}'.")

			for statementBin in statementBins:
				if not isinstance(statementBin, etree._Element):
					raise InternalErrorOccurred(f"Unexpected type: '{statementBin.__class__.__name__}'.")

				nodes.append(statementBin)

		statements: DefaultDict[str, DefaultDict[int, List]] = defaultdict(lambda: defaultdict(list))

		for node in nodes:
			workdir, stmtData = self._parseStatementNode(node)
			self._coverage.addSource(workdir)

			flags = node.get("flags")

			if flags is None:
				raise InternalErrorOccurred("Unexpected 'None' value.")

			if int(flags, 16) & UCDB_EXCLUDED:
				_ = statements[stmtData.file]
				continue

			statements[stmtData.file][stmtData.line].append(stmtData)

		for file, lines in statements.items():
			package = Package(file)
			coberturaClass = Class(file, file)
			package.addClass(coberturaClass)
			self._coverage.addPackage(package)

			for line, lineStmts in lines.items():
				if self._mergeInstances:
					lineStmts = self._groupByIndex(lineStmts)

				self.statementsCount += len(lineStmts)

				covered = len(list(filter(attrgetter("hits"), lineStmts)))
				hit = int(covered == len(lineStmts))

				self.statementsCovered += covered

				coberturaClass.addStatement(line, hit)

	def _parseStatementNode(self, node) -> Tuple[str, StatementData]:
		srcNode = node.find("./ux:src", namespaces=self._nsmap)
		workdir = srcNode.get("workdir")

		instancePath = ".".join(
			(scope.get("name") for scope in node.iterancestors("{*}scope"))
		)

		stmtIndex = int(
			node.find("./ux:attr[@key='#SINDEX#']", namespaces=self._nsmap).text
		)

		count = int(node.find("./ux:count", namespaces=self._nsmap).text)

		stmtData = StatementData(
			file=srcNode.get("file"),
			line=int(srcNode.get("line")),
			index=stmtIndex,
			instance=instancePath,
			hits=count,
		)

		return workdir, stmtData
