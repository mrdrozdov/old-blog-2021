import unittest

from kiss import DAG


class TestKiss(unittest.TestCase):
    def test_order(self):
        tasks = [
            dict(name='a', depends=[]),
            dict(name='c', depends=['b']),
            dict(name='b', depends=['a']),
        ]

        order = DAG(tasks, strict=False).iterate_over_tasks()
        expected = ['a', 'b', 'c']

        self.assertEqual(order, expected)

    def test_cycle(self):
        tasks = [
            dict(name='a', depends=['c']),
            dict(name='c', depends=['b']),
            dict(name='b', depends=['a']),
        ]

        with self.assertRaises(RuntimeError) as context:
            order = DAG(tasks, strict=False).iterate_over_tasks()

        error_message = context.exception.args[0]
        expected = 'Cycle detected.'

        self.assertEqual(error_message, expected)

    def test_strict(self):
        tasks = [
            dict(name='a', depends=[]),
        ]

        with self.assertRaises(KeyError):
            order = DAG(tasks, strict=True)
        

if __name__ == '__main__':
    unittest.main()
