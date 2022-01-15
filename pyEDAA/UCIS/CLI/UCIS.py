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
Tools to extract data from UCIS datafiles.

.. topic:: Usage

.. code-block::

   acdb2xml -i aggregate.acdb -o ucdb.xml
   python ucdb2cobertura.py -i ucdb.xml -o cobertura.xml
"""
from lxml import etree

from pyEDAA.UCIS.Cobertura import Coverage


class UcdbParser:
	def __init__(self, filename):
		file = open(filename)
		self.tree = etree.parse(filename)
		file.close()

		self.nsmap = self.tree.getroot().nsmap

		self.coverage = Coverage()

	def get_cobertura_model(self):
		self.parse_statement_coverage()

		return self.coverage

	def parse_statement_coverage(self):
		nodes = self.tree.xpath("//ux:bin[@type='STMTBIN']", namespaces=self.nsmap)
		for node in nodes:
			self.parse_statement_node(node)

	def parse_statement_node(self, node):
		count = int(node.find("./ux:count", namespaces=self.nsmap).text)
		src_node = node.find("./ux:src", namespaces=self.nsmap)
		file_name = src_node.get("file")
		source = src_node.get("workdir")
		line = int(src_node.get("line"))

		self.coverage.add_statement(source, file_name, line, count)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="Input UCDB XML file")
	parser.add_argument("-o", "--output", help="Output Cobertura XML file")

	args = parser.parse_args()

	parser = UcdbParser(args.input)
	model = parser.get_cobertura_model()

	with open(args.output, 'w') as output_file:
		output_file.write(model.get_xml().decode("utf-8"))

	print("Covered {}% of statements".format(model.lines_covered / model.lines_valid * 100))
