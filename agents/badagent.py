class BadAgent:

    def __init__(self):
        self.name = 'Bad Agent'

    def load_payoff_conditions(self, payoffs):
        """
        Load the payoffs in the form of a 2x2 matrix.
        Ex:
        [
            [(-1, -1), (-3, 0)],
            [(0, -3), (-2, -2)]
        ]

        Will be called by simulator.
        """
        self.payoffs = payoffs

    def play_round(self, last_round_results):
        """
        Take the results of last round and make a decision about what to do
        this round.

        Last round results are a string of the form 'C' or 'D' to
        indicate what the opponent did.
        If None, then it's the first round.

        Will be called by simulator.
        """
        return 'D'
