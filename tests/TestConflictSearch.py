import unittest

import itertools

from conflictenum import ConflictEnum
from planner import Planner
from plan import Plan
from level import Level
from pprint import pprint


class TestConflictSearch(unittest.TestCase):

    def setUp(self):
        self.level = Level([],[],[],[],0,0)
        self.planner = Planner(self.level)
        # self.planner = planner.planner(self.level)

    def tearDown(self):
        self.planner = None
        self.level = None

    def test_find_conflicts_from_plan(self):
        plan_a = Plan()
        plan_a.path = [ ((0,1), 0), ((0,2), 1), ((0,3), 2) ]

        plan_b = Plan()
        plan_b.path = [ ((1,0), 0), ((1,1), 1), ((0,1), 2) ]

        plan_c = Plan()
        plan_c.path = [ ((0,3), 0), ((0,2), 1), ((0,1), 2) ]

        plan_list = (plan_a, plan_b, plan_c)
        
        conflicts = [ (ConflictEnum.SameCell, (plan_a, plan_c), [((0,2), 1)]), ( ConflictEnum.SameCell, (plan_b, plan_c), [((0,1), 2)]) ]


        test = self.planner.find_conflicts_from_plans(plan_list)

        # pprint(test)

        self.assertEqual(conflicts, test)

    def test_min_conflict_list(self):
        plan_a = Plan()
        plan_a.path = [ ((0,1), 0), ((0,2), 1), ((0,3), 2)]

        plan_b = Plan()
        plan_b.path = [ ((0,1), 0), ((1,1), 1), ((0, 1), 2)]

        plan_c = Plan()
        plan_c.path = [ ((0,1), 0), ((0,2), 1), ((0,1), 2) ]

        plan_list = (plan_a, plan_b, plan_c)
        
        conflicts = [   (ConflictEnum.SameCell, (plan_a, plan_b), [((0,1), 0)]),
                        (ConflictEnum.SameCell, (plan_a, plan_c), [((0,1), 0)]),
                        (ConflictEnum.SameCell, (plan_b, plan_c), [((0,1), 0)])
                    ]

        min_conflicts = self.planner.find_conflicts_from_plans(plan_list)

        # pprint(test)

        # min_conflicts = self.planner.find_min_conflicts(test)

        # pprint(test)
        # print("")
        # pprint(conflicts)
        # print("")
        # pprint(min_conflicts)

        self.assertEqual(conflicts, min_conflicts)

    def test_swapping_conflict_finding(self):
        plan_a = Plan()
        plan_a.path = [ ((0,1), 0), ((0,2), 1), ((0,3), 2)]

        plan_b = Plan()
        plan_b.path = [ ((0,4), 0), ((0,3), 1), ((0, 2), 2)]

        plan_list = (plan_a, plan_b)

        onflicts = self.planner.find_swapping(plan_list)

        # pprint(conflicts)


if __name__ == '__main__':
    unittest.main()