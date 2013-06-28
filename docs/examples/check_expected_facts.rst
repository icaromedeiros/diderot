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

To test if the expected facts are indeed inferred by the given ontology we can implement this simple Python code:

.. literalinclude :: ../../example/test/test_expected_facts.py
    :lines: 1-9

Now consider that we add the triple ``example:Icaro a example:Student`` to the expected facts file.

It is quite obvious that this fact can not be inferred from the ontology.
Then, when running the tests, an ``AssertionError`` will be raised with the expected facts that could not be inferred.

.. code-block:: console

   $ make test
   ======================================================================
   FAIL: test_some_expected_facts_can_not_be_inferred (test.test_expected_facts.ExpectedFactsTestCase)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "/path_to_test/test_expected_facts.py", line 16, in test_some_expected_facts_can_not_be_inferred
       self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))
     File "/path_to_diderot/diderot/case.py", line 37, in assertThat
       raise AssertionError(ASSERTION_ERROR_MESSAGE.format(not_inferred_graph.serialize(format="nt")))
   AssertionError: Could not infer some expected facts:
     <http://example.onto/Icaro> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.onto/Student>.
