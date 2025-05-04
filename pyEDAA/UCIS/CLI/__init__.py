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
# Copyright 2021-2025 Electronic Design Automation Abstraction (EDA²)                                                  #
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
from argparse import RawDescriptionHelpFormatter, Namespace
from pathlib  import Path
from textwrap import dedent
from typing   import Optional as Nullable

from pyTooling.Decorators                     import export
from pyTooling.Attributes.ArgParse            import ArgParseHelperMixin, DefaultHandler, CommandHandler
from pyTooling.Attributes.ArgParse.Argument   import StringArgument
from pyTooling.Attributes.ArgParse.ValuedFlag import LongValuedFlag
from pyTooling.Attributes.ArgParse.Flag       import LongFlag
from pyTooling.TerminalUI                     import TerminalApplication

from pyEDAA.UCIS           import __version__, __copyright__, __license__
from pyEDAA.UCIS.UCDB      import Parser
from pyEDAA.UCIS.Cobertura import CoberturaException


@export
class ProgramBase(TerminalApplication):
	"""Base-class for all program classes."""

	programTitle: str

	def __init__(self) -> None:
		pass

	def _PrintHeadline(self) -> None:
		"""Print the program's headline."""
		print("{line}".format(line="=" * 120))
		print("{headline: ^120s}".format(headline=self.programTitle))
		print("{line}".format(line="=" * 120))


@export
class Application(ProgramBase, ArgParseHelperMixin):
	"""Program class to implement the command line interface (CLI) using commands and options."""

	programTitle = "UCDB Service Program"

	def __init__(self) -> None:
		super().__init__()

		# Call the constructor of the ArgParseMixin
		ArgParseHelperMixin.__init__(
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
		ArgParseHelperMixin.Run(self)

	@DefaultHandler()
	def HandleDefault(self, _: Namespace) -> None:
		"""Handle program calls without any command."""
		self._PrintHeadline()
		self._PrintHelp()

	@CommandHandler("help", help="Display help page(s) for the given command name.", description="Display help page(s) for the given command name.")
	@StringArgument(dest="Command", metaName="Command", optional=True, help="Print help page(s) for a command.")
	def HandleHelp(self, args: Namespace) -> None:
		"""Handle program calls with command ``help``."""
		self._PrintHeadline()
		self._PrintHelp(args.Command)

	@CommandHandler("version", help="Display version information.", description="Display version information.")
	def HandleVersion(self, _: Namespace) -> None:
		"""Handle program calls with command ``version``."""
		self._PrintHeadline()
		self._PrintVersion()


	def _PrintVersion(self) -> None:
		"""Helper function to print the version information."""
		print(dedent(f"""\
			Copyright: {__copyright__}
			License:   {__license__}
			Version:   v{__version__}
			""")
		)

	def _PrintHelp(self, command: Nullable[str] = None) -> None:
		"""Helper function to print the command line parsers help page(s)."""
		if command is None:
			self.MainParser.print_help()
		elif command == "help":
			print("This is a recursion ...")
		else:
			try:
				self.SubParsers[command].print_help()
			except KeyError:
				print(f"Command {command} is unknown.")

	@CommandHandler("export", help="Export data from UCDB.", description="Export data from UCDB.")
	@LongValuedFlag("--ucdb",      dest="ucdb",      metaName='UCDBFile',      help="UCDB file in UCIS format (XML).")
	@LongValuedFlag("--cobertura", dest="cobertura", metaName='CoberturaFile', help="Cobertura code coverage file (XML).")
	@LongFlag("--merge-instances", dest="mergeInstances", help="Merge statement coverage data for all instances of the same design unit.")
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

		parser = Parser(ucdbPath, args.mergeInstances)
		model = parser.getCoberturaModel()

		with coberturaPath.open('w') as file:
			file.write(model.getXml().decode("utf-8"))

		print()

		try:
			lineCoverage = model.linesCovered / model.linesValid * 100
		except ZeroDivisionError:
			lineCoverage = 100

		try:
			statementCoverage = parser.statementsCovered / parser.statementsCount * 100
		except ZeroDivisionError:
			statementCoverage = 100

		print(dedent(f"""\
			[DONE] Export and conversion complete.
			  Line coverage: {lineCoverage} %
			  Statement coverage: {statementCoverage} %
			""")
		)

	def _PrintVersion(self) -> None:
		"""Helper function to print the version information."""
		print(dedent(f"""\
			Copyright: {__copyright__}
			License:   {__license__}
			Version:   v{__version__}
			""")
		)

	def _PrintHelp(self, command: Nullable[str] = None) -> None:
		"""Helper function to print the command line parsers help page(s)."""
		if command is None:
			self.MainParser.print_help()
		elif command == "help":
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
	from sys import argv

	program = Application()
	program.Configure(
		verbose=("-v" in argv or "--verbose" in argv),
		debug=("-d" in argv or "--debug" in argv),
		quiet=("-q" in argv or "--quiet" in argv)
	)
	try:
		program.Run()
	except CoberturaException as ex:
		program.WriteLineToStdErr(f"{{RED}}[ERROR] {ex}{{NOCOLOR}}".format(**Application.Foreground))
		if ex.__cause__ is not None:
			program.WriteLineToStdErr(f"{{DARK_YELLOW}}Because of: {ex.__cause__}{{NOCOLOR}}".format(**Application.Foreground))

	except NotImplementedError as ex:
		program.PrintNotImplementedError(ex)
	except Exception as ex:
		program.PrintException(ex)


if __name__ == "__main__":
	main()
