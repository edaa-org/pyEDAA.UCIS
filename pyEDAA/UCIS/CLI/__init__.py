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
Tools to extract data from UCDB files.

.. rubric:: Usage

First export/convert the Aldec Coverage Database (ACDB) into UCDB (Universal Coverage Database) format. The
helper program ``acdb2xml`` (part of Active-HDL or Riviera-PRO installation) can be used.

.. code-block::

   acdb2xml -i aggregate.acdb -o ucdb.xml

At next use this layer's service program to convert from UCDB to Cobertura format.

.. code-block::

   pyedaa-ucis export --ucdb ucdb.xml --cobertura cobertura.xml
"""
from argparse import RawDescriptionHelpFormatter
from pathlib  import Path
from textwrap import dedent

from pyAttributes.ArgParseAttributes import ArgParseMixin, DefaultAttribute, CommandAttribute, ArgumentAttribute
from pyTooling.Decorators import export

from pyEDAA.UCIS      import __version__, __copyright__, __license__
from pyEDAA.UCIS.UCDB import Parser


@export
class ProgramBase():
	"""Base-class for all program classes."""

	programTitle = "UCDB Service Program"

	def __init__(self) -> None:
		pass

	def _PrintHeadline(self) -> None:
		"""Print the programs headline."""
		print("{line}".format(line="=" * 120))
		print("{headline: ^120s}".format(headline=self.programTitle))
		print("{line}".format(line="=" * 120))


@export
class Program(ProgramBase, ArgParseMixin):
	"""Program class to implement the command line interface (CLI) using commands and options."""

	def __init__(self) -> None:
		super().__init__()

		# Call the constructor of the ArgParseMixin
		ArgParseMixin.__init__(
			self,
			prog="pyedaa-ucis",
		  description=dedent('''\
				'pyEDAA.UCIS Service Program' to query and transform data to/from UCIS to any other format.
				'''),
		  epilog=dedent("""\
		    Currently the following output formats are supported:
		     * Cobertura (statement coverage - Java oriented format)
		  """),
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
		"""Handle program calls without any command."""
		self._PrintHeadline()
		self._PrintHelp()

	@CommandAttribute("help", help="Display help page(s) for the given command name.", description="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args) -> None:
		"""Handle program calls with command ``help``."""
		self._PrintHeadline()
		self._PrintHelp(args.Command)

	@CommandAttribute("version", help="Display version information.", description="Display version information.")
	def HandleVersion(self, _) -> None:
		"""Handle program calls with command ``version``."""
		self._PrintHeadline()
		self._PrintVersion()

	@CommandAttribute("export", help="Export data from UCDB.", description="Export data from UCDB.")
	@ArgumentAttribute("--ucdb",      metavar='UCDBFile',      dest="ucdb",      type=str, help="UCDB file in UCIS format (XML).")
	@ArgumentAttribute("--cobertura", metavar='CoberturaFile', dest="cobertura", type=str, help="Cobertura code coverage file (XML).")
	def HandleExport(self, args) -> None:
		"""Handle program calls with command ``export``."""
		self._PrintHeadline()

		returnCode = 0
		if args.ucdb is None:
			print(f"Option '--ucdb <UCDBFile' is missing.")
			returnCode = 3
		if args.cobertura is None:
			print(f"Option '--cobertura <CoberturaFile' is missing.")
			returnCode = 3

		if returnCode != 0:
			exit(returnCode)

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

	def _PrintVersion(self):
		"""Helper function to print the version information."""
		print(dedent(f"""\
			Copyright: {__copyright__}
			License:   {__license__}
			Version:   v{__version__}
			""")
		)

	def _PrintHelp(self, command: str=None):
		"""Helper function to print the command line parsers help page(s)."""
		if (command is None):
			self.MainParser.print_help()
		elif (command == "help"):
			print("This is a recursion ...")
		else:
			try:
				self.SubParsers[command].print_help()
			except KeyError:
				print(f"Command {command} is unknown.")


@export
def main():
	"""
	Entrypoint to start program execution.

	This function should be called either from:
	 * ``if __name__ == "__main__":`` or
	 * ``console_scripts`` entry point configured via ``setuptools`` in ``setup.py``.

	This function creates an instance of :class:`Program` in a ``try ... except`` environment. Any exception caught is
	formatted and printed before the program returns with a non-zero exit code.
	"""
	program = Program()
	try:
		program.Run()
	except FileNotFoundError as ex:
		print()
		print(f"[ERROR] {ex}")
		exit(1)


if __name__ == "__main__":
	main()
