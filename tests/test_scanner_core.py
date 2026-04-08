import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

import scanner_core

# Fixtures to provide reusable mock setups
@pytest.fixture
def mock_file_system():
    """Simulates a directory structure without touching the real filesystem."""
    files = {
        '/test/path/config.json': '{"secret": "12345"}',
        '/test/path/readme.txt': 'No secrets here',
        '/test/path/secret.txt': 'API_KEY: abc-123-def',
        '/test/path/image.png': 'binary data',
    }
    with patch('os.walk') as mock_walk, \
         patch('builtins.open', new_callable=MagicMock) as mock_open:
        
        mock_walk.return_value = iter([
            ('/test/path', [], ['config.json', 'readme.txt', 'secret.txt', 'image.png'])
        ])
        
        def side_effect(filename, *args, **kwargs):
            content = files.get(filename, '')
            return Mock(read=Mock(return_value=content))
        
        mock_open.return_value.__enter__.return_value = Mock(side_effect=side_effect)
        
        yield {
            'path': '/test/path',
            'files': files,
            'walk': mock_walk,
            'open': mock_open
        }

@pytest.fixture
def mock_requests():
    """Mocks the external API calls."""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        yield mock_post

@pytest.fixture
def scan_config():
    return {
        'path': '/test/path',
        'extensions': ['.json', '.txt', '.py'],
        'patterns': [r'API_KEY\s*:\s*[\w-]+', r'secret.*:.*\w+'],
        'api_endpoint': 'https://api.scanner.dev/upload'
    }

# Tests for scan_directory
class TestScanDirectory:
    def test_scan_directory_returns_files(self, mock_file_system):
        result = scanner_core.scan_directory(mock_file_system['path'], extensions=['.json', '.txt'])
        assert len(result) == 3  # json, txt, secret.txt
        assert '/test/path/config.json' in result
        assert '/test/path/secret.txt' in result
        assert '/test/path/image.png' not in result

    def test_scan_directory_filters_extensions(self, mock_file_system):
        # Ensure .png is excluded as per extension list
        result = scanner_core.scan_directory(mock_file_system['path'], extensions=['.txt'])
        assert len(result) == 1
        assert '/test/path/secret.txt' in result
        assert '/test/path/config.json' not in result

    def test_scan_directory_path_error(self):
        with patch('scanner_core.os.path.exists', return_value=False):
            result = scanner_core.scan_directory('/nonexistent/path', extensions=['.txt'])
            assert result == []

# Tests for read_file
class TestReadFile:
    def test_read_file_content_success(self, mock_file_system):
        content = scanner_core.read_file('/test/path/secret.txt')
        assert 'API_KEY' in content
        assert 'abc-123-def' in content

    def test_read_file_content_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                scanner_core.read_file('/does/not/exist.txt')

    def test_read_file_content_empty(self, mock_file_system):
        # Simulate empty file logic
        content = scanner_core.read_file('/test/path/readme.txt')
        assert content == 'No secrets here'
        assert len(content) > 0

# Tests for check_patterns
class TestCheckPatterns:
    @patch('re.compile')
    def test_detect_secrets_found(self, mock_compile, scan_config):
        mock_re = Mock()
        mock_re.search.return_value = Mock(group=Mock(return_value='API_KEY: abc-123-def'))
        mock_compile.return_value = mock_re
        
        result = scanner_core.check_patterns('API_KEY: abc-123-def', scan_config['patterns'])
        assert len(result) > 0
        assert 'API_KEY' in str(result[0])

    def test_detect_secrets_not_found(self):
        result = scanner_core.check_patterns('This is safe content', [r'password.*\d{4}'])
        assert len(result) == 0