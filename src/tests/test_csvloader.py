import unittest
from unittest.mock import patch, Mock
from secondary_adapters.csvloader import load_dataset
from logic.movie import Movie
from main_types import Config

class TestLoadDataset(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            logger=Mock(),
            workspace_path="",
        )  
    
    # See https://stackoverflow.com/questions/1289894/how-do-i-mock-an-open-used-in-a-with-statement-using-the-mock-framework-in-pyth 
    # for info on mocking the open built in
    @patch('builtins.open')
    def test_load_dataset_success(self, mock_open):
        # Arrange
        csv_data = '''record_id,movie_id,title,country,release_year,description,vector_embedding
1,1,"Movie 1",US,2020,"Description 1","[0.1, 0.2, 0.3]"
2,2,"Movie 2",UK,2021,"Description 2","[0.4, 0.5, 0.6]"'''
        mock_open.return_value.__enter__.return_value = csv_data.splitlines()

        # Act
        result = load_dataset('dataset.csv', self.config)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Movie)
        self.assertIsInstance(result[1], Movie)
        self.config.logger.debug.assert_called_once_with("loaded 2 records")
        self.config.logger.warning.assert_not_called()

    @patch('builtins.open')
    def test_load_dataset_error(self, mock_open):
        # Arrange
        csv_data = '''record_id,movie_id,title,country,release_year,description,vector_embedding
1,1,"Movie 1",US,2020,"Description 1","[0.1, 0.2, 0.3]"
2,2,"Movie 2",UK,invalid_year,"Description 2","[0.4, 0.5, 0.6]"'''
        mock_open.return_value.__enter__.return_value = csv_data.splitlines()

        # Act
        result = load_dataset('dataset.csv', self.config)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Movie)
        self.config.logger.debug.assert_called_once_with("loaded 1 records")
        self.config.logger.warning.call_count == 2 
        self.config.logger.warning.assert_called_with("encountered 1 error(s)")

if __name__ == '__main__':
    unittest.main()