import warnings

from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Horn.HornRules import HornFromN3
from FuXi.Rete.Util import generateTokenSet

from diderot.utils import get_empty_graph
from diderot import rules

warnings.filterwarnings("ignore")


def build_rdfs_owl_rules():
    """
        Utility function that loads ``RDFS`` and ``OWL`` semantics in
        a ``FuXi`` ``RETE.Network`` object.
    """
    rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
    rdfs_rules = HornFromN3(rules.__path__[0] + "/rdfs_rules.n3")
    for rule in rdfs_rules:
        network.buildNetworkFromClause(rule)

    owl_rules = HornFromN3(rules.__path__[0] + "/owl_rules.n3")
    for rule in owl_rules:
        try:
            network.buildNetworkFromClause(rule)
        except:
            pass  # TODO ignoring FuXi errors
    return network



#: This attribute is loaded on ``diderot`` import to build ``RDFS`` and
#: ``OWL`` rules only one time.
RDFS_OWL_RULES = build_rdfs_owl_rules()


class Inference():
    """
        Class that wraps ``FuXi`` ``RETE.Network`` to hold
        the network of facts, trigger inference, and
        retrieve inferred facts.
    """

    def __init__(self):
        """
            The ``Inference`` object is loaded with ``RDFS`` and
            ``OWL`` rules (``diderot.inference.RDFS_OWL_RULES``) and an empty
            graph to hold inferred facts.
        """
        self.network = RDFS_OWL_RULES
        self.network.inferredFacts = get_empty_graph()

    def add_facts(self, facts):
        """
            Add facts (a ``RDFlib.Graph`` object) to inference network
            thus triggering the inference.
        """
        self.network.feedFactsToAdd(generateTokenSet(facts))

    def get_inferred_facts(self):
        """
            Get inferred facts from network.
        """
        return self.network.inferredFacts
