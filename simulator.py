from constants import agents_dir, payoffs, rounds, min_rounds, max_rounds

import itertools

from os import listdir
from os.path import isfile, join

import importlib

import random


def collect_agents():
    agents = [f for f in listdir(agents_dir) if
              isfile(join(agents_dir, f)) and
              not ('template' in f.lower())]
    return agents


def load_agents(agent_files):
    """
    Loading a dynamically named class is actually harder than it looks, so
    this is some Python witchcraft to do that.
    """
    agents = []

    for a in agent_files:

        # Grab the module
        # Need to strip out .py, hence the [:-3]
        agent_module = importlib.import_module('agents.'+a[:-3])

        # find_class
        # Now we can find the class as part of that module
        agent_class_name = [
            x for x in dir(agent_module) if
            not ('template' in x.lower()) and not ('__' in x)
            ][0]
        agent_class = getattr(agent_module, agent_class_name)

        # instantiate
        agent = agent_class()
        agents.append(agent)

    return agents


def score_helper(agent1_action, agent2_action, payoffs):
    """
    Computes the score for each agent given an action combo.
    """

    if agent1_action == 'C' and agent2_action == 'C':
        # Both cooperate
        return payoffs[0][0]
    elif agent1_action == 'D' and agent2_action == 'C':
        # Agent 1 backstab
        return payoffs[1][0]
    elif agent1_action == 'C' and agent2_action == 'D':
        # Agent 2 backstab
        return payoffs[0][1]
    else:
        # Both defect
        return payoffs[1][1]


def run_match(agent1, agent2, rounds, payoffs):
    """
    Takes two agents, has them play against each other for a given number of
    rounds.

    Returns the total score for each agent as a tuple.
    """

    agent1_last_action = None
    agent2_last_action = None

    agent1_score = 0
    agent2_score = 0

    for r in range(rounds):
        try:
            agent1_action = agent1.play_round(agent2_last_action)
        except Exception as e:
            # On error, award penalize maximum points
            return (payoffs[0][1][0] * rounds, 0)

        try:
            agent2_action = agent2.play_round(agent1_last_action)
        except Exception as e:
            # On error, award penalize maximum points
            return (0, payoffs[0][1][0] * rounds)

        # compute payoff
        scores = score_helper(agent1_action, agent2_action, payoffs)

        agent1_score += scores[0]
        agent2_score += scores[1]

        agent1_last_action = agent1_action
        agent2_last_action = agent2_action

    return agent1_score, agent2_score


def run_tournament(agents, randomize_round_num=True):
    """
    Runs a tournament with all the agents.
    """

    for a in agents:
        try:
            a.load_payoff_conditions(payoffs)
        except Exception as e:
            pass

    score_dict = {}

    for a in agents:
        score_dict[a.name] = 0

    for (a1, a2) in itertools.product(agents, agents):

        if randomize_round_num:
            match_rounds = random.randint(min_rounds, max_rounds)
        else:
            match_rounds = rounds

        (a1_score, a2_score) = run_match(a1, a2, match_rounds, payoffs)

        score_dict[a1.name] += a1_score
        score_dict[a2.name] += a2_score

    return score_dict
