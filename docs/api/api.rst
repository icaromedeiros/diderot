Diderot API
===========

Here we document Diderot's programming interface

:mod:`DiderotTestCase` class
----------------------------

.. autoclass:: diderot.DiderotTestCase
    :members: assert_that

:mod:`assertion` module
-----------------------

.. automodule:: diderot.assertion
    :members: can_infer, can_answer

.. autoclass:: diderot.assertion.Assertion
    :members:

    .. automethod:: __init__

.. autoclass:: diderot.assertion.InferenceAssertion
   :members:

   .. automethod:: __init__

.. autoclass:: diderot.assertion.CompetencyQuestionAssertion
   :members:

   .. automethod:: __init__

:mod:`inference` module
-----------------------

.. automodule:: diderot.inference
    :members: build_rdfs_owl_rules, RDFS_OWL_RULES

.. autoclass:: diderot.inference.Inference
    :members:

    .. automethod:: __init__

:mod:`utils` module
-------------------

.. automodule:: diderot.utils
    :members:

:mod:`OWL` module
-----------------

.. automodule:: diderot.OWL
