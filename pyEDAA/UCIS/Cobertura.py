from datetime import time

from lxml import etree


class Class:
	def __init__(self, source_file: str):
		self.source_file = source_file  # type: str
		self.lines = {}  # type: dict[int, int]
		self.lines_valid = 0  # type: int
		self.lines_covered = 0  # type: int

	def add_statement(self, line: int, count: int) -> None:
		assert line not in self.lines.keys()
		self.lines[line] = count
		self.lines_valid += 1
		if count:
			self.lines_covered += 1

	def get_xml_node(self) -> etree.Element:
		class_node = etree.Element("class")
		class_node.attrib["name"] = self.source_file
		class_node.attrib["filename"] = self.source_file
		class_node.attrib["complexity"] = "0"
		class_node.attrib["branch-rate"] = "0"
		class_node.attrib["line-rate"] = str(self.lines_covered / self.lines_valid)
		class_node.append(etree.Element("methods"))
		lines_node = etree.SubElement(class_node, "lines")

		for line in self.lines:
			etree.SubElement(
				lines_node,
				"line",
				number=str(line),
				hits=str(self.lines[line]),
			)

		return class_node


class Package:
	def __init__(self, name: str):
		self.name = name  # type: str
		self.classes = {}  # type: dict[str, Class]
		self.lines_valid = 0  # type: int
		self.lines_covered = 0  # type: int

	def add_statement(self, class_name: str, source_file: str, line: int, count: int) -> None:
		try:
			self.classes[class_name].add_statement(line, count)
		except KeyError:
			self.classes[class_name] = Class(source_file)
			self.classes.get(class_name).add_statement(line, count)

		self.lines_valid += 1

		if count:
			self.lines_covered += 1

	def get_xml_node(self) -> etree.Element:
		classes_node = etree.Element("classes")
		package_node = etree.Element("package")
		package_node.append(classes_node)
		package_node.attrib["name"] = self.name
		package_node.attrib["complexity"] = "0"
		package_node.attrib["branch-rate"] = "0"
		package_node.attrib["line-rate"] = str(self.lines_covered / self.lines_valid)

		for (class_name, class_data) in self.classes.items():
			classes_node.append(class_data.get_xml_node())

		return package_node


class Coverage:
	def __init__(self):
		self.sources = set()  # type: set
		self.packages = {}  # type: dict[str, Package]
		self.lines_valid = 0  # type: int
		self.lines_covered = 0  # type: int

	def add_statement(self, source: str, file: str, line: int, count: int) -> None:
		try:
			self.packages[source].add_statement(file, file, line, count)
		except KeyError:
			self.packages[source] = Package(file)
			self.packages.get(source).add_statement(file, file, line, count)

		self.sources.add(source)

		self.lines_valid += 1

		if count:
			self.lines_covered += 1

	def add_branch(self) -> None:
		pass

	def get_xml(self) -> etree.Element:
		coverage_node = etree.Element("coverage")
		coverage_node.attrib["version"] = "5.5"
		coverage_node.attrib["timestamp"] = str(int(time()))
		coverage_node.attrib["branches-valid"] = "0"
		coverage_node.attrib["branches-covered"] = "0"
		coverage_node.attrib["branch-rate"] = "0"
		coverage_node.attrib["complexity"] = "0"
		coverage_node.attrib["lines-valid"] = str(self.lines_valid)
		coverage_node.attrib["lines-covered"] = str(self.lines_covered)
		coverage_node.attrib["line-rate"] = str(self.lines_covered / self.lines_valid)

		sources_node = etree.Element("sources")

		for source in self.sources:
			etree.SubElement(sources_node, "source").text = source

		coverage_node.append(sources_node)

		packages_node = etree.Element("packages")

		for package_name in self.packages:
			packages_node.append(self.packages[package_name].get_xml_node())

		coverage_node.append(packages_node)

		return etree.tostring(coverage_node, pretty_print=True, encoding="utf-8", xml_declaration=True)
