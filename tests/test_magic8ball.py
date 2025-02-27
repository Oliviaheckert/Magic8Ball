import pytest
from magic8ball import Magic8Ball
from unittest.mock import patch
import json
import os

@pytest.fixture
def mock_ball():
    return Magic8Ball()

def test_answer_distribution(mock_ball):
    categories = []
    for _ in range(1000):
        answer = mock_ball._get_answer("test")
        categories.append(next(
            k for k, v in mock_ball.responses.items() 
            if answer in v
        ))
    
    pos = categories.count('positive') / 1000
    assert 0.35 < pos < 0.45  # Verify 40% weight

def test_session_save(mock_ball, tmp_path):
    mock_ball.history.append({
        'question': "test",
        'answer': "Yes",
        'timestamp': "2023-01-01T00:00:00"
    })
    
    with patch('os.getcwd', return_value=str(tmp_path)):
        mock_ball._save_session()
    
    saved_files = os.listdir(tmp_path)
    assert len(saved_files) == 1
    assert saved_files[0].startswith('8ball_session_')

def test_empty_stats(mock_ball):
    with patch('builtins.print') as mock_print:
        mock_ball._show_help()
        mock_ball.main()
    
    mock_ball._show_help()
    mock_ball._show_stats()
    assert "No answers yet!" in mock_print.call_args_list[1][0][0]
