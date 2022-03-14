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
"""
Data model of the Cobertura format.

.. mermaid::

   flowchart LR
     Coverage --> Package --> Class --> Statement

"""
from time import time
from typing import Dict, Set

from lxml import etree
from pyTooling.Decorators import export


@export
class CoberturaException(Exception):
	"""Base-class for other Cobertura exceptions"""


@export
class DuplicatedLineNumber(CoberturaException):
	"""Raised when statement with specified line number already exists in Cobertura class"""


@export
class DuplicatedClassName(CoberturaException):
	"""Raised when class with specified name already exists in Cobertura package"""


@export
class DuplicatedPackageName(CoberturaException):
	"""Raised when package with specified name already exists in Cobertura coverage"""


@export
class Class:
	"""Represents a code element in the Cobertura coverage data model (Java-focused)."""

	name: str
	sourceFile: str
	lines: Dict[int, int]
	linesValid: int
	linesCovered: int

	def __init__(self, name: str, sourceFile: str):
		self.name = name
		self.sourceFile = sourceFile
		self.lines = {}
		self.linesValid = 0
		self.linesCovered = 0

	def addStatement(self, line: int, hits: int) -> None:
		if line in self.lines.keys():
			raise DuplicatedLineNumber(f"Duplicated line number: {line}")

		self.lines[line] = hits
		self.linesValid += 1

		if hits:
			self.linesCovered += 1

	def getXmlNode(self) -> etree._Element:
		classNode = etree.Element("class")
		classNode.attrib["name"] = self.sourceFile
		classNode.attrib["filename"] = self.sourceFile
		classNode.attrib["complexity"] = "0"
		classNode.attrib["branch-rate"] = "0"

		try:
			rate = self.linesCovered / self.linesValid
		except ZeroDivisionError:
			rate = 1.0

		classNode.attrib["line-rate"] = f"{rate:.16g}"

		classNode.append(etree.Element("methods"))
		linesNode = etree.SubElement(classNode, "lines")

		for line in self.lines:
			etree.SubElement(
				linesNode,
				"line",
				number=str(line),
				hits=str(self.lines[line]),
			)

		return classNode


@export
class Package:
	"""Represents a grouping element in the Cobertura coverage data model (Java-focused)."""

	name: str
	classes: Dict[str, Class]
	linesValid: int
	linesCovered: int

	def __init__(self, name: str):
		self.name = name
		self.classes = {}
		self.linesValid = 0
		self.linesCovered = 0

	def addClass(self, coberturaClass: Class):
		if coberturaClass.name in self.classes:
			raise DuplicatedClassName(f"Duplicated class name: '{coberturaClass.name}'.")

		self.classes[coberturaClass.name] = coberturaClass

	def refreshStatistics(self) -> None:
		self.linesValid = 0
		self.linesCovered = 0

		for coberturaClass in self.classes.values():
			self.linesCovered += coberturaClass.linesCovered
			self.linesValid += coberturaClass.linesValid

	def getXmlNode(self) -> etree._Element:
		classesNode = etree.Element("classes")
		packageNode = etree.Element("package")
		packageNode.attrib["name"] = self.name
		packageNode.attrib["complexity"] = "0"
		packageNode.attrib["branch-rate"] = "0"

		try:
			rate = self.linesCovered / self.linesValid
		except ZeroDivisionError:
			rate = 1.0

		packageNode.attrib["line-rate"] = f"{rate:.16g}"

		packageNode.append(classesNode)

		for coberturaClass in self.classes.values():
			classesNode.append(coberturaClass.getXmlNode())

		return packageNode


@export
class Coverage:
	"""Represents the root element in the Cobertura coverage data model (Java-focused)."""

	sources: Set
	packages: Dict[str, Package]
	linesValid: int
	linesCovered: int

	def __init__(self):
		self.sources = set()
		self.packages = {}
		self.linesValid = 0
		self.linesCovered = 0

	def addSource(self, source: str) -> None:
		self.sources.add(source)

	def addPackage(self, package: Package) -> None:
		if package.name in self.packages:
			raise DuplicatedPackageName(f"Duplicated package name: '{package.name}'.")

		self.packages[package.name] = package

	def refreshStatistics(self) -> None:
		self.linesValid = 0
		self.linesCovered = 0

		for package in self.packages.values():
			package.refreshStatistics()
			self.linesCovered += package.linesCovered
			self.linesValid += package.linesValid

	def getXml(self) -> bytes:
		self.refreshStatistics()

		coverageNode = etree.Element("coverage")
		coverageNode.attrib["version"] = "5.5"
		coverageNode.attrib["timestamp"] = str(int(time()))
		coverageNode.attrib["branches-valid"] = "0"
		coverageNode.attrib["branches-covered"] = "0"
		coverageNode.attrib["branch-rate"] = "0"
		coverageNode.attrib["complexity"] = "0"

		sourcesNode = etree.Element("sources")

		for source in self.sources:
			etree.SubElement(sourcesNode, "source").text = source

		coverageNode.append(sourcesNode)

		packagesNode = etree.Element("packages")

		for package in self.packages.values():
			packagesNode.append(package.getXmlNode())

		coverageNode.append(packagesNode)

		coverageNode.attrib["lines-valid"] = str(self.linesValid)
		coverageNode.attrib["lines-covered"] = str(self.linesCovered)

		try:
			rate = self.linesCovered / self.linesValid
		except ZeroDivisionError:
			rate = 1.0

		coverageNode.attrib["line-rate"] = f"{rate:.16g}"

		return etree.tostring(
			coverageNode, pretty_print=True, encoding="utf-8", xml_declaration=True
		)
