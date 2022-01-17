Code Coverage
#############

Statement Coverage
******************

.. code-block:: Bash

   # Convert ACDB file into UCDB file (XML format)
   acdb2xml -i aggregate.acdb -o ucdb.xml

   # Convert UCDB file into Cobertura format
   pyedaa-ucis export --ucdb ucdb.xml --cobertura cobertura.xml

Branch Coverage
***************

.. note:: Branch coverage isn't supported yet.
