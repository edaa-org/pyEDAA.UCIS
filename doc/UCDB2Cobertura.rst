UCDB2Cobertura
##############

.. code-block:: Bash

   # Convert ACDB file into UCDB file (XML format)
   acdb2xml -i aggregate.acdb -o ucdb.xml

   # Convert UCDB file into Cobertura format
   python ucdb2cobertura.py -i ucdb.xml -o cobertura.xml
