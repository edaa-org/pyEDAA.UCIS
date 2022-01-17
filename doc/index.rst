.. include:: shields.inc

.. image:: _static/logo.svg
   :height: 90 px
   :align: center
   :target: https://GitHub.com/edaa-org/pyEDAA.UCIS

.. raw:: html

    <br>

.. raw:: latex

   \part{Introduction}

.. only:: html

   |  |SHIELD:svg:UCIS-github| |SHIELD:svg:UCIS-src-license| |SHIELD:svg:UCIS-ghp-doc| |SHIELD:svg:UCIS-doc-license| |SHIELD:svg:UCIS-gitter|
   |  |SHIELD:svg:UCIS-pypi-tag| |SHIELD:svg:UCIS-pypi-status| |SHIELD:svg:UCIS-pypi-python|
   |  |SHIELD:svg:UCIS-gha-test| |SHIELD:svg:UCIS-lib-status| |SHIELD:svg:UCIS-codacy-quality| |SHIELD:svg:UCIS-codacy-coverage| |SHIELD:svg:UCIS-codecov-coverage|

.. Disabled shields: |SHIELD:svg:UCIS-lib-dep| |SHIELD:svg:UCIS-req-status| |SHIELD:svg:UCIS-lib-rank|

.. only:: latex

   |SHIELD:png:UCIS-github| |SHIELD:png:UCIS-src-license| |SHIELD:png:UCIS-ghp-doc| |SHIELD:png:UCIS-doc-license| |SHIELD:png:UCIS-gitter|
   |SHIELD:png:UCIS-pypi-tag| |SHIELD:png:UCIS-pypi-status| |SHIELD:png:UCIS-pypi-python|
   |SHIELD:png:UCIS-gha-test| |SHIELD:png:UCIS-lib-status| |SHIELD:png:UCIS-codacy-quality| |SHIELD:png:UCIS-codacy-coverage| |SHIELD:png:UCIS-codecov-coverage|

.. Disabled shields: |SHIELD:png:UCIS-lib-dep| |SHIELD:png:UCIS-req-status| |SHIELD:png:UCIS-lib-rank|

The pyEDAA.UCIS Documentation
#############################

Unified Coverage Interoperability Standard (UCIS).

.. image:: _static/work-in-progress.png
   :height: 275 px
   :align: center
   :target: https://GitHub.com/edaa-org/pyEDAA.UCIS

.. raw:: html

    <br>


.. _goals:

Main Goals
**********

* Parse UCDB files and provide a UCDB data model.
* Export and convert code coverage information from UCDB to Cobertura format.
* Also support flavors not following the Unified Coverage Interoperability Standard (UCIS).


.. _usecase:

Use Cases
*********

* Collect and merge code coverage with Active-HDL / Riviera-PRO and convert via UCDB format to Cobertura files, so
  code coverage can be published to e.g. GitLab, Codacy or CodeCov.


.. _contributors:

Contributors
************

* `Patrick Lehmann <https://GitHub.com/Paebbels>`__ (Maintainer)
* `Artur Porebski (Aldec Inc.) <https://github.com/por3bski>`__
* `Michal Pacula (Aldec Inc.) <https://github.com/mikep996>`__
* `Unai Martinez-Corral <https://GitHub.com/umarcor/>`__
* `and more... <https://GitHub.com/edaa-org/pyEDAA.UCIS/graphs/contributors>`__


.. _license:

License
*******

.. only:: html

   This Python package (source code) is licensed under `Apache License 2.0 <Code-License.html>`__. |br|
   The accompanying documentation is licensed under `Creative Commons - Attribution 4.0 (CC-BY 4.0) <Doc-License.html>`__.

.. only:: latex

   This Python package (source code) is licensed under **Apache License 2.0**. |br|
   The accompanying documentation is licensed under **Creative Commons - Attribution 4.0 (CC-BY 4.0)**.


.. toctree::
   :hidden:

   Used as a layer of EDA² ➚ <https://edaa-org.github.io/>

.. toctree::
   :caption: Introduction
   :hidden:

   Installation
   Dependency

.. raw:: latex

   \part{Main Documentation}

.. toctree::
   :caption: Main Documentation
   :hidden:

   CodeCoverage

.. raw:: latex

   \part{References}

.. toctree::
   :caption: References
   :hidden:

   CommandLineInterface
   pyEDAA.UCIS/index

.. raw:: latex

   \part{Appendix}

.. toctree::
   :caption: Appendix
   :hidden:

   Coverage Report ➚ <coverage/index>
   Static Type Check Report ➚ <typing/index>
   License
   Doc-License
   Glossary
   genindex

.. #
   py-modindex
