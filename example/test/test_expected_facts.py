from diderot import DiderotTestCase, can_infer


class ExpectedFactsTestCase(DiderotTestCase):

    def test_check_expected_facts(self):
        EXPECTED_FACTS_FILE = "example/db/check_expected_facts/expected_facts.n3"
        ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
        self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))

    # Just to show error messages
    def test_check_expected_facts(self):
        EXPECTED_FACTS_FILE = "example/db/check_expected_facts/expected_facts.n3"
        ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
        self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))

    def test_check_expected_facts(self):
        EXPECTED_FACTS_FILE = "example/db/check_expected_facts/expected_facts.n3"
        ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
        self.assertThat(can_infer(EXPECTED_FACTS_FILE).from_facts(ONTOLOGY_FILE))