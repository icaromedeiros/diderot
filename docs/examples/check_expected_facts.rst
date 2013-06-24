Checking expected inferred facts
================================

In this example we can check if expected facts can be inferred from the ontology.

Consider this simple ontology:

.. literalinclude :: ../../example/db/check_expected_facts/ontology.n3
    :language: n3
    :emphasize-lines: 4-5

It says that ``Human`` is a sub class of ``Mortal``, and that ``Icaro`` is a human.
From this one can simply infer that ``Icaro`` is mortal.

Moreover, as the domain and range of the property ``rdfs:subClassOf`` is ``rdfs:Class`` and ``owl:Class`` is sub class of ``rdfs:Class``, both ``Mortal`` and ``Human`` are instances of ``owl:Class``. So, the expected facts are:

.. literalinclude :: ../../example/db/check_expected_facts/expected_facts.n3
    :language: n3
    :emphasize-lines: 4-6
