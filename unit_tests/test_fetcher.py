import unittest
from unittest.mock import patch, mock_open
from src.fetcher import Fetcher

class TestFetcherWithMocks(unittest.TestCase):
    def setUp(self):
        self.fetcher = Fetcher()

    def test_get_column_type(self):
        self.assertEqual(Fetcher.get_column_type('123'), float)
        self.assertEqual(Fetcher.get_column_type('123.45'), float)
        self.assertEqual(Fetcher.get_column_type('hello'), str)
        self.assertEqual(Fetcher.get_column_type('-42'), float)

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='name,age,score\nAlice,25,85.5\nBob,30,92.3')
    def test_fetch_data_with_mocks(self, mock_file, mock_listdir):
        mock_listdir.return_value = ['test1.csv']
        result = self.fetcher.fetch_data(None, None, False, None)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Alice')
        self.assertEqual(result[0]['age'], '25')
        mock_file.assert_called_once()

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='name,age,score\nAlice,25,85.5\nBob,30,92.3')
    def test_fetch_data_with_filters(self, mock_file, mock_listdir):
        mock_listdir.return_value = ['test1.csv']
        result = self.fetcher.fetch_data([('age', '>', '25')], None, False, None)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Bob')

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open,
           read_data='name,age,score\nAlice,25,85.5\nBob,30,92.3\nCharlie,22,78.1')
    def test_fetch_data_with_sorting(self, mock_file, mock_listdir):
        mock_listdir.return_value = ['test1.csv']
        result = self.fetcher.fetch_data(sort='age', reverse=False)

        self.assertEqual(result[0]['name'], 'Charlie')
        self.assertEqual(result[1]['name'], 'Alice')
        self.assertEqual(result[2]['name'], 'Bob')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.join')
    def test_export_data(self, mock_path_join, mock_file):
        test_data = [{'name': 'Test', 'value': 42}]
        mock_path_join.return_value = '/mock/path/output.json'
        self.fetcher.export_data(test_data)

        mock_file.assert_called_once_with('/mock/path/output.json', 'w')
        handle = mock_file()
        handle.write.assert_called_once()
        written_content = handle.write.call_args[0][0]
        self.assertTrue(written_content.startswith('['))
        self.assertTrue(written_content.endswith(']\n'))

    def test_row_matches_filters(self):
        row = {'age': '25', 'score': '85.5'}

        self.assertTrue(self.fetcher.row_matches_filters(row, [('age', '==', '25')]))
        self.assertTrue(self.fetcher.row_matches_filters(row, [('age', '>', '24')]))
        self.assertFalse(self.fetcher.row_matches_filters(row, [('age', '>', '30')]))
        self.assertTrue(self.fetcher.row_matches_filters(row, [('age', '>', '20'), ('age', '<', '30')]))
        with self.assertRaises(ValueError):
            self.fetcher.row_matches_filters(row, [('age', '===', '25')])

    def test_get_analytics(self):
        sample_data = [
            {'name': 'Alice', 'age': '25', 'score': '85.5'},
            {'name': 'Bob', 'age': '30', 'score': '92.3'},
            {'name': 'Charlie', 'age': '22', 'score': '78.1'}
        ]
        numeric_stats, categorical_counts = Fetcher.get_analytics(sample_data)

        self.assertIn('age', numeric_stats)
        self.assertAlmostEqual(numeric_stats['age']['mean'], 25.666666, places=2)
        self.assertEqual(numeric_stats['age']['max'], 30)
        self.assertEqual(numeric_stats['age']['min'], 22)
        self.assertIn('name', categorical_counts)
        self.assertEqual(len(categorical_counts['name']), 3)

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_error_handling_in_fetch_data(self, mock_file, mock_listdir):
        mock_listdir.return_value = ['test1.csv', 'test2.csv']
        mock_file.side_effect = [
            mock_open(read_data='name,age\nAlice,25')(),  # First file works
            Exception("Simulated file error")  # Second file raises an error
        ]

        with patch('builtins.print') as mock_print:
            result = self.fetcher.fetch_data(None, None, False, None)

            mock_print.assert_called_once_with("Error processing file test2.csv : Simulated file error")
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['name'], 'Alice')

if __name__ == '__main__':
    unittest.main()
