from math import log2
from typing import List
from graph.models.outcome import Outcome

def calculateProbability(outcome: Outcome, totalOutcomes: int):
    return (outcome.Quantity / totalOutcomes) if totalOutcomes != 0 else 0


def calculateEntropy(outcomes: List[Outcome], totalOutcomes: int):
    entropy = 0.0
    
    # print("\n" + "-" * 10)
    for item in outcomes:
        # Calculate probability of (x) address occurring
        prob = calculateProbability(item, totalOutcomes)

        # print("\nName: {0}\tQty: {1}\tProb: {2}".format(item.Name, item.Quantity, prob))

        # Calculate entropy of the system at time y
        step = prob * log2(prob)

        # Sum the outcomes
        entropy += step

    return abs(entropy)