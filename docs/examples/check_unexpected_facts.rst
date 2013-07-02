Checking unexpected inferred facts
===================================

In this example we can check if unexpected inferred facts cannot be inferred from the ontology.

Consider this simple ontology (the same one used in :doc:`check_expected_facts`)\:

.. literalinclude :: ../../example/db/check_expected_facts/ontology.n3
    :language: n3

It says that ``Human`` is a sub class of ``Mortal``, and that ``Icaro`` is a human.
From this one can simply infer that ``Icaro`` is mortal.

Moreover, as the domain and range of the property ``rdfs:subClassOf`` is ``rdfs:Class`` and ``owl:Class`` is sub class of ``rdfs:Class``, both ``Mortal`` and ``Human`` are instances of ``owl:Class``.

We want to be sure that ``example:Icaro a example:Student`` cannot be inferred. We use the code below:

.. literalinclude :: ../../example/test/test_unexpected_facts.py
    :language: python
    :lines: 1-9, 18-23

This is useful in a stage of ontology development that we have not added ``example:Student`` to the ontology yet but in the future it will exist, so this test will fail, or can be changed to use ``can_infer()`` instead of ``cannot_infer()``.

Now we want to see the test fail adding a fact we know it can be inferred, such as ``example:Icaro a example:Mortal .``.


.. code-block:: console

   $ make test
   ======================================================================
   FAIL: test_check_unexpected_facts_fail (test.test_unexpected_facts.ExpectedFactsTestCase)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "/path/test_unexpected_facts.py", line 16, in test_check_unexpected_facts_fail
       self.assert_that(cannot_infer(UNEXPECTED_FACTS).from_facts(ONTOLOGY_FILE))
     File "/path/diderot/case.py", line 30, in assert_that
       raise AssertionError(assertion.assertion_error_message)
   AssertionError: Could infer some unexpected facts:

     <http://example.onto/Icaro> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>
        <http://example.onto/Mortal>.
   ----------------------------------------------------------------------
