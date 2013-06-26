[![Build Status](https://secure.travis-ci.org/icaromedeiros/diderot.png)](http://travis-ci.org/icaromedeiros/diderot)
[![Coverage Status](https://coveralls.io/repos/icaromedeiros/diderot/badge.png?branch=master)](https://coveralls.io/r/icaromedeiros/diderot?branch=master)

Diderot is a framework for Test Driven Development of RDF/OWL ontologies.

Learn how to build maintainable and flexible yet SOUND and COMPLETE ontologies using a test, refactor, and retest cycle.

The documentation is available at http://diderot.readthedocs.org

Installing
==========

To install Diderot one can simply...


A quick example
=================

Checking expected facts
-----------------------

In this example we can check if expected facts can be inferred from the ontology. Consider this simple ontology:

```
:Human rdfs:subClassOf :Mortal .
:Icaro a :Human .
```

It says that ``Human`` is a sub class of ``Mortal``, and that ``Icaro`` is a human.
From this one can simply infer that ``Icaro`` is mortal.

Moreover, as the domain and range of the property ``rdfs:subClassOf`` is ``rdfs:Class`` and ``owl:Class`` is sub class of ``rdfs:Class``, both ``Mortal`` and ``Human`` are instances of ``owl:Class``. So, the expected facts are:

```
:Icaro a :Mortal .
:Mortal a owl:Class .
:Human a owl:Class .
```

To test if the expected facts are indeed inferred by the given ontology we can implement this simple Python code:

```python
from diderot import DiderotTestCase, can_infer


class ExpectedFactsTestCase(DiderotTestCase):

    def test_check_expected_facts(self):
        EXPECTED_FACTS_FILE = "path/to/expected_facts.n3"
        ONTOLOGY_FILE = "path/to/ontology.n3"
        self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))
```

More examples on: http://diderot.readthedocs.org
