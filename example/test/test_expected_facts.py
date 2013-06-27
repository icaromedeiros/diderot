from diderot import DiderotTestCase, can_infer


class ExpectedFactsTestCase(DiderotTestCase):

    def test_check_expected_facts(self):
        EXPECTED_FACTS_FILE = "example/db/check_expected_facts/expected_facts.n3"
        ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
        self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))

    # Just to show error messages

    #def test_some_expected_facts_can_not_be_inferred(self):
    #    EXPECTED_FACTS_FILE = "example/db/check_expected_facts/could_not_infer_all_expected_facts.n3"
    #    ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
    #    self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))

    #def test_check_expected_facts_unkown_file(self):
    #    EXPECTED_FACTS_FILE = "test/unkown_file.n3"
    #    self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(EXPECTED_FACTS_FILE))

    #def test_check_expected_facts_unkown_protocol(self):
    #    EXPECTED_FACTS_URI = "ftp://www.uknown.com"
    #    self.assertThat(can_infer(EXPECTED_FACTS_URI).from_facts(EXPECTED_FACTS_URI))

    #def test_check_expected_facts_malformed_turtle(self):
    #    EXPECTED_FACTS_STRING = """
    #    :Icaro a :Human ;
    #    :Icaro a :Mortal ;
    #    """
    #    self.assertThat(can_infer(EXPECTED_FACTS_STRING).from_facts(EXPECTED_FACTS_STRING))
