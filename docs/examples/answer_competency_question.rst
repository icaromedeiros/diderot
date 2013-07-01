Answering competency questions
==============================

In this example we can ask to ontologies questions we expect them to answer.

Consider this simple ontology:

.. literalinclude :: ../../example/db/answering_competency_question/ontology.n3
    :language: n3

It states that humans (instances of ``example:Human``) can have name and age.
Moreover, it defines an instance of ``example:Human``, ``example:Icaro``, that has a name ``Icaro`` and age of ``26``.
So, we might want to check if the ontology can answer: is there any humans with the properties names and ages?

In Diderot we can check this by using this simple Python code below.
In lines ``7-14`` we translated the question stated before as a SPARQL query.
Then, in line ``16``, we call ``self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE))`` with an ontology file and a question as parameters to check if the ontology can answer the given question.

.. literalinclude :: ../../example/test/test_competency_question_answering.py
    :language: python
    :linenos:
    :lines: 1, 3-16

Only ``SELECT`` and ``ASK`` queries are accepted.
The test will pass if the query result is not empty (for ``SELECT`` queries) or ``True`` (for ``ASK`` queries).

An example of a test that fail if we ask to the aforementioned ontology if there is any god (that don't exist, at least in the database)\:

.. code-block:: console

   $ make test
   ======================================================================
   FAIL: test_check_can_answer_with_ask_returns_false (test.test_competency_question_answering.ExpectedFactsTestCase)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File /path_to_test/test_competency_question_answering.py", line 51, in test_check_can_answer_with_ask_returns_false
       self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE))
     File /path_to_test/case.py", line 30, in assert_that
       raise AssertionError(assertion.assertion_error_message)
   AssertionError: ASK query returned false.
     Query:
           ASK {
               ?god a <http://example.onto/God> .
           }


However, in this case we only wanted to check if the ontology **can** answer the question.
Another useful use case is to check if the ontology can answer the question with a **specific expected answer**.

This can be done with the Python code below.
The new thing is the argument ``EXPECTED_ANSWER`` passed to ``with_answer()``.
It states expected results for the SPARQL query as a list of tuples of python primitive types (``int``, ``string``, etc) or a ``RDFlib.URIRef`` for URIs.
The tuples should follow the order of the variables in the ``SELECT`` clause in the SPARQL query.
So, the tuple ``(URIRef("http://example.onto/Icaro"), 26, "Icaro")`` match the variables ``?human, ?age, ?name``, respectively.

.. literalinclude :: ../../example/test/test_competency_question_answering.py
    :language: python
    :linenos:
    :lines: 1-4, 28-40

If expected answers and query results are not equal, the test will fail:

.. code-block:: console

   $ make test
   ======================================================================
   FAIL: test_check_can_answer_with_answer_dont_match_expected_answer (test.test_competency_question_answering.ExpectedFactsTestCase)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "/Users/icaro.medeiros/workspace/diderot/example/test/test_competency_question_answering.py", line 75, in test_check_can_answer_with_answer_dont_match_expected_answer
       with_answer(EXPECTED_ANSWER))
     File "/Users/icaro.medeiros/workspace/diderot/diderot/case.py", line 30, in assert_that
       raise AssertionError(assertion.assertion_error_message)
   AssertionError: Query result is different from expected answer.
     given
   X = [(rdflib.URIRef('http://example.onto/Icaro'), rdflib.Literal(u'26', datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema#integer')), rdflib.Literal(u'Icaro'))]
       and
   Y = [(rdflib.URIRef('http://example.onto/Icaro'), 64, 'Icaro Medeiros')]
   X[0][1] is rdflib.Literal(u'26', datatype=rdflib.URIRef('http://www.w3.org/2001/XMLSchema#integer')) whereas Y[0][1] is 64

Note that the query result returns a ``rdflib.Literal`` object, that is transformed to a python primitive type (such as ``int`` or ``string``) when trying to compare with expected answers if it is not a URI reference.
