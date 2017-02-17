import unittest
from src.montecarlo import get_totals, run_simulation, SIMULATION_RUN_COUNT, create_table


class TestMonteCarlo(unittest.TestCase):
    """Tests for `montecarlo.py`."""

    def test_get_totals(self):
        """Does the get_totals function sum values correctly?"""
        tasks = [
            {"minimum": 1, "maximum": 2, "estimate": 3},
            {"minimum": 4, "maximum": 5, "estimate": 6},
            {"minimum": 7, "maximum": 8, "estimate": 9},
            ]
        minimum, maximum, estimate = get_totals(tasks)
        self.assertEqual(minimum, 12)
        self.assertEqual(maximum, 15)
        self.assertEqual(estimate, 18)

    def test_simulation_ordered(self):
        """Is the result of the simulation ordered?"""
        minimum, maximum = 1, 10
        result = run_simulation(minimum, maximum)
        for i, key in enumerate(result):
            self.assertEqual(key, i + 1)

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

    def test_simulation_result_contains_correct_keys(self):
        minimum, maximum = 1, 10
        result = run_simulation(minimum, maximum)
        for i in range(minimum, maximum + 1):
            self.assertTrue(i in result)
    

if __name__ == '__main__':
    unittest.main()
