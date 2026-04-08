import sys
import pytest
import unittest.mock as mock
import argparse
from io import StringIO

import cli_interface


@pytest.fixture
def mock_args(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['dev-scanner', '--target', './src', '--format', 'json'])
    return sys.argv


@pytest.fixture
def mock_stdin(monkeypatch, input_text):
    monkeypatch.setattr(sys, 'stdin', StringIO(input_text))


@pytest.fixture
def mock_api(monkeypatch):
    with mock.patch.object(cli_interface, 'scanning_api') as mock_scan:
        mock_scan.scan_secrets.return_value = [{'type': 'password', 'confidence': 0.9}]
        yield mock_scan


class TestParseCliArgs:

    def test_parse_args_with_target_and_format(self, mock_args):
        args = cli_interface.parse_cli_args()
        assert args.target == './src'
        assert args.format == 'json'

    def test_parse_args_with_default_values(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['dev-scanner'])
        args = cli_interface.parse_cli_args()
        assert args.target is None
        assert args.format == 'text'

    def test_parse_args_invalid_format(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['dev-scanner', '--format', 'xml'])
        with pytest.raises(SystemExit):
            cli_interface.parse_cli_args()


class TestHandleUserInteraction:

    def test_interact_confirm_scan(self, monkeypatch, mock_stdin):
        monkeypatch.setattr(sys, 'argv', ['dev-scanner', '-y'])
        input_text = ''  # --yes flag skips interaction
        result = cli_interface.handle_user_interaction({'verbose': True})
        assert result is True

    def test_interact_user_decline(self, monkeypatch, mock_stdin):
        input_text = 'n\n'
        monkeypatch.setattr(sys, 'argv', ['dev-scanner'])
        result = cli_interface.handle_user_interaction()
        assert result is False

    def test_inter