from policies.dql.mlp_policy import MLPPolicy
from policies.dql.base_policy import DQNPolicy
from policies.dql.nate_policy import NATEPolicy
from policies.dql.ctnate_policy import CTNATEPolicy

from policies.ga.nsga_policy import NSGA2Policy
from policies.ga.npga_policy import NPGAPolicy

from policies.heuristics.random import RandomPolicy
from policies.heuristics.greedy import GreedyPolicy
from policies.heuristics.round_robin import RoundRobinPolicy


policies = {
    "MLP": MLPPolicy,
    "T-MLP": MLPPolicy,

    "NATE": NATEPolicy,
    "T-NATE": NATEPolicy,
    "CT-NATE": CTNATEPolicy,

    "NPGA": NPGAPolicy,
    "NSGA2": NSGA2Policy,

    "Greedy": GreedyPolicy,
    "Random": RandomPolicy,
    "RoundRobin": RoundRobinPolicy,
}
