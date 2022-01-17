# ==================================================================================================================== #
#               _____ ____    _        _     _   _  ____ ___ ____                                                      #
#   _ __  _   _| ____|  _ \  / \      / \   | | | |/ ___|_ _/ ___|                                                     #
#  | '_ \| | | |  _| | | | |/ _ \    / _ \  | | | | |    | |\___ \                                                     #
#  | |_) | |_| | |___| |_| / ___ \  / ___ \ | |_| | |___ | | ___) |                                                    #
#  | .__/ \__, |_____|____/_/   \_\/_/   \_(_)___/ \____|___|____/                                                     #
#  |_|    |___/                                                                                                        #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
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

.. rubric:: Usage

First export/convert the Aldec Coverage Database (ACDB) into UCIS format (Universal Coverage Database - UCDB). The
helper program ``acdb2xml`` (part of Active-HDL or Riviera-PRO installation) can be used.

.. code-block::

   acdb2xml -i aggregate.acdb -o ucdb.xml

At next use this layer's service program to convert from UCIS to Cobertura format.

.. code-block::

   python ucdb2cobertura.py -i ucdb.xml -o cobertura.xml
"""
from argparse import RawDescriptionHelpFormatter
from pathlib import Path
from textwrap import dedent, fill

from pyAttributes.ArgParseAttributes import ArgParseMixin, DefaultAttribute, CommandAttribute, ArgumentAttribute

from pyEDAA.UCIS.UCDB import Parser


class ProgramBase():
	programTitle = "UCDB service program"

	def __init__(self) -> None:
		pass

	def _PrintHeadline(self) -> None:
		print("{line}".format(line="=" * 120))
		print("{headline: ^80s}".format(headline=self.programTitle))
		print("{line}".format(line="=" * 120))


class Program(ProgramBase, ArgParseMixin):
	def __init__(self) -> None:
		super().__init__()

		# Call the constructor of the ArgParseMixin
		ArgParseMixin.__init__(
			self,
			prog="pyedaa-ucis",
		  description=dedent('''\
				Query and transform data to/from UCIS to any format.
				'''),
		  epilog=fill("Query and transform data to/from UCIS to any format."),
		  formatter_class=RawDescriptionHelpFormatter,
		  add_help=False
		)

#	@CommonSwitchArgumentAttribute("-q", "--quiet",   dest="quiet",   help="Reduce messages to a minimum.")
#	@CommonSwitchArgumentAttribute("-v", "--verbose", dest="verbose", help="Print out detailed messages.")
#	@CommonSwitchArgumentAttribute("-d", "--debug",   dest="debug",   help="Enable debug mode.")
	def Run(self) -> None:
		ArgParseMixin.Run(self)

	@DefaultAttribute()
	def HandleDefault(self, _) -> None:
		self._PrintHeadline()
		self._PrintHelp()

	@CommandAttribute("help", help="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args) -> None:
		self._PrintHeadline()
		self._PrintHelp(args.Command)

	@CommandAttribute("export", help="Export data from UCDB.")
	@ArgumentAttribute(metavar='<UCDB File>',      dest="ucdb",      type=str, help="UCDB file in UCIS format (XML).")
	@ArgumentAttribute(metavar='<Cobertura File>', dest="cobertura", type=str, help="Cobertura code coverage file (XML).")
	def HandleExport(self, args) -> None:
		self._PrintHeadline()

		print(f"Exporting code coverage information from UCDB file to Cobertura format ...")

		ucdbPath = Path(args.ucdb)
		if not ucdbPath.exists():
			raise FileNotFoundError(f"UCDB databse file '{ucdbPath}' not found.")

		coberturaPath = Path(args.cobertura)

		print(f"  IN  -> UCIS (XML):      {ucdbPath}")
		print(f"  OUT <- Cobertura (XML): {coberturaPath}")

		parser = Parser(ucdbPath)
		model = parser.get_cobertura_model()

		with coberturaPath.open('w') as file:
			file.write(model.get_xml().decode("utf-8"))

		print()

		coverage = model.lines_covered / model.lines_valid * 100
		print(dedent(f"""\
			[DONE] Export and conversion complete.
			  Statement coverage: {coverage} %
			""")
		)


	def _PrintHelp(self, command: str=None):
		if (command is None):
			self.MainParser.print_help()
		elif (command == "help"):
			print("This is a recursion ...")
		else:
			try:
				self.SubParsers[command].print_help()
			except KeyError:
				print(f"Command {command} is unknown.")


def main():
	program = Program()
	try:
		program.Run()
	except FileNotFoundError as ex:
		print()
		print(f"[ERROR] {ex}")
		exit(1)


if __name__ == "__main__":
	main()
