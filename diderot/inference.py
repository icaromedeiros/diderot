import warnings

from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Horn.HornRules import HornFromN3
from FuXi.Rete.Util import generateTokenSet

from diderot.utils import get_empty_graph
from diderot import rules

warnings.filterwarnings("ignore")


def build_rdfs_owl_rules():
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


RDFS_OWL_RULES = build_rdfs_owl_rules()


class Inference():

    def __init__(self):
        self.network = RDFS_OWL_RULES
        closureDeltaGraph = get_empty_graph()
        self.network.inferredFacts = closureDeltaGraph

    def add_facts(self, facts):
        self.network.feedFactsToAdd(generateTokenSet(facts))

    def get_inferred_facts(self):
        return self.network.inferredFacts
