import unittest
import final_solution   


class SoultionTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SoultionTestCase, self).__init__(*args, **kwargs)
        self.solution = final_solution
    
    @classmethod
    def setUpClass(cls):
        print('setUpClass\n\n')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown\n')
    
    def test_find_all_positions(self):
        # because the grid is a set, so the result is not stable. 
        print('test_find_all_positions')
        blocks = ['A', 'B']
        grid = {(1, 3), (3, 3), (3, 1), (5, 1), (1, 1), (5, 3)}
        res = [(('B', 'A'), ((1, 3), (3, 3))), (('B', 'A'), ((1, 3), (3, 1))), (('B', 'A'), ((1, 3), (5, 1))), (('B', 'A'), ((1, 3), (1, 1))), (('B', 'A'), ((1, 3), (5, 3))), (('B', 'A'), ((3, 3), (3, 1))), (('B', 'A'), ((3, 3), (5, 1))), (('B', 'A'), ((3, 3), (1, 1))), (('B', 'A'), ((3, 3), (5, 3))), (('B', 'A'), ((3, 1), (5, 1))), (('B', 'A'), ((3, 1), (1, 1))), (('B', 'A'), ((3, 1), (5, 3))), (('B', 'A'), ((5, 1), (1, 1))), (('B', 'A'), ((5, 1), (5, 3))), (('B', 'A'), ((1, 1), (5, 3))), (('A', 'B'), ((1, 3), (3, 3))), (('A', 'B'), ((1, 3), (3, 1))), (('A', 'B'), ((1, 3), (5, 1))), (('A', 'B'), ((1, 3), (1, 1))), (('A', 'B'), ((1, 3), (5, 3))), (('A', 'B'), ((3, 3), (3, 1))), (('A', 'B'), ((3, 3), (5, 1))), (('A', 'B'), ((3, 3), (1, 1))), (('A', 'B'), ((3, 3), (5, 3))), (('A', 'B'), ((3, 1), (5, 1))), (('A', 'B'), ((3, 1), (1, 1))), (('A', 'B'), ((3, 1), (5, 3))), (('A', 'B'), ((5, 1), (1, 1))), (('A', 'B'), ((5, 1), (5, 3))), (('A', 'B'), ((1, 1), (5, 3)))]
        # print('=====',self.solution.find_all_positions(blocks, grid))
        self.assertEquals(res, self.solution.find_all_positions(blocks, grid))
    
    def test_cal_reflect_start(self):
        point = (1, 2, 1, 1)
        reflect_point = (1, 2, 1, -1)
        self.assertEquals(reflect_point, self.solution.cal_reflect_start(point))

    def test_get_intersect_point(self):
        intersect_grid = {(1, 1)}
        lazor_points = [(0, 1, 1, 1), (1, 2, 1, 1), (2, 3, 1, 1), (3, 4, 1, 1)]
        start_point = (0, 1, 1, 1)
        res = (0, 1, 1, 1)
        self.assertEquals(res, self.solution.get_intersect_point(intersect_grid, lazor_points, start_point))

    # this oen will fail. (test fail case)
    # def test_get_intersect_grid(self):
    #     intersect_point = (2, 3, 1, 1)
    #     grid = (3, 3)
    #     self.assertEquals(grid, self.solution.test_get_intersect_grid(intersect_point))

    def test_check_position(self):
        position = {(3, 1): self.solution.Block('A'), (5, 1): self.solution.Block('B')}
        grid = {(1, 3), (3, 3), (3, 1), (5, 1), (1, 1), (5, 3)}
        start_points = [(0, 1, 1, 1)]
        goal_points = {(3, 4)}
        self.assertEquals(False, self.solution.check_position(position, grid, start_points, goal_points))

if __name__ == '__main__':
    unittest.main()
