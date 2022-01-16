from argparse import RawDescriptionHelpFormatter
from textwrap import dedent, fill
from typing   import Callable, Any

from pyAttributes.ArgParseAttributes import ArgParseMixin, CommonSwitchArgumentAttribute, DefaultAttribute, CommandAttribute, ArgumentAttribute


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
	@CommonSwitchArgumentAttribute("-v", "--verbose", dest="verbose", help="Print out detailed messages.")
	@CommonSwitchArgumentAttribute("-d", "--debug",   dest="debug",   help="Enable debug mode.")
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

		print(dedent(f"""\
			HandleExport ...
			  UCDB:      {args.ucdb}
			  Cobertura: {args.cobertura}
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
	program.Run()


if __name__ == "__main__":
	main()
