import unittest

import itertools

from conflictenum import ConflictEnum
from planner import Planner
from plan import Plan
from level import Level
from pprint import pprint


from action import ActionType, Action


class TestActionFinding(unittest.TestCase):

    def setUp(self):
        self.level = Level([],[],[],[],0,0)
        self.planner = Planner(self.level)
        # self.planner = planner.planner(self.level)

    def tearDown(self):
        self.planner = None
        self.level = None

    def test_find_conflicts_from_plan_ES(self):

        agent_coord = (0, 0)
        box_coord = (1, 0)
        box_next_coord = (1, 1)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushES, given_action)


    def test_find_conflicts_from_plan_EN(self):

        agent_coord = (0, 1)
        box_coord = (1, 1)
        box_next_coord = (1, 0)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushEN, given_action)

    def test_find_conflicts_from_plan_WN(self):

        agent_coord = (1, 1)
        box_coord = (0, 1)
        box_next_coord = (0, 0)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushWN, given_action)

    def test_find_conflicts_from_plan_WS(self):

        agent_coord = (1, 0)
        box_coord = (0, 0)
        box_next_coord = (0, 1)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushWS, given_action)

    def test_find_conflicts_from_plan_SE(self):
        agent_coord = (0, 0)
        box_coord = (0, 1)
        box_next_coord = (1, 1)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushSE, given_action)

    def test_find_conflicts_from_plan_SW(self):

        agent_coord = (1, 0)
        box_coord = (1, 1)
        box_next_coord = (0, 1)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushSW, given_action)

    def test_find_conflicts_from_plan_NE(self):

        agent_coord = (0, 1)
        box_coord = (0, 0)
        box_next_coord = (1, 0)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushNE, given_action)

    def test_find_conflicts_from_plan_NW(self):

        agent_coord = (1, 1)
        box_coord = (1, 0)
        box_next_coord = (0, 0)
        # expected_action = ActionType.PushES

        # print(expected_action)

        _,given_action = self.planner.determine_action(agent_coord, box_coord, box_next_coord)


        print(given_action)

        self.assertEqual(Action.PushNW, given_action)





if __name__ == '__main__':
    unittest.main()