# Usage:
# acdb2xml -i aggregate.acdb -o ucdb.xml
# python ucdb2cobertura.py -i ucdb.xml -o cobertura.xml


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
