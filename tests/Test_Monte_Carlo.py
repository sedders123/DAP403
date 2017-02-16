import unittest
from src.montecarlo import get_totals, run_simulation, SIMULATION_RUN_COUNT


class TestMonteCarlo(unittest.TestCase):
    """Tests for `montecarlo.py`."""

    def test_get_totals(self):
        """Does the get_totals function sum values correctly?"""
        tasks = [
            {"minimum": 1, "maximum": 2},
            {"minimum": 3, "maximum": 4},
            {"minimum": 5, "maximum": 6}
            ]
        minimum, maximum = get_totals(tasks)
        self.assertEquals(minimum, 9)
        self.assertEquals(maximum, 12)

    def test_simulation_ordered(self):
        """Is the result of the simulation ordered?"""
        minimum, maximum = 1, 10
        result = run_simulation(minimum, maximum)
        for i, key in enumerate(result):
            self.assertEquals(key, i + 1)

    def test_simulation_values_greater_than_previous(self):
        """ Do the results of each simulated step include results of previous steps?"""
        minimum, maximum = 1, 10
        result = run_simulation(minimum, maximum)
        result_values = list(result.values())
        for i, value in enumerate(result.values()):
            if i == 0:
                return
            self.assertTrue(result_values[i]["number"] >= result_values[i-1]["number"])

    def test_simulation_runs_correct_amount_of_times(self):
        """Does the simulation run the correct number of times?"""
        minimum, maximum = 1, 10
        result = run_simulation(minimum, maximum)
        self.assertTrue(SIMULATION_RUN_COUNT in [value["number"] for value in result.values()])


if __name__ == '__main__':
    unittest.main()
