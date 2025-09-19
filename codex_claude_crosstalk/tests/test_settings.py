"""
Tests for the configuration system.
"""

import pytest
import os
import tempfile
import yaml
from unittest.mock import patch, mock_open

from codex_claude_crosstalk.config.settings import Settings


class TestSettings:
    """Test cases for Settings configuration management."""
    
    def test_default_initialization(self):
        """Test initialization with default values."""
        settings = Settings()
        
        assert settings.claude_config["model"] == "claude-3-sonnet"
        assert settings.codex_config["model"] == "code-davinci-002"
        assert settings.templates_config["default_language"] == "python"
        assert settings.logging_config["level"] == "INFO"
        
    def test_initialization_with_config(self):
        """Test initialization with custom config."""
        config = {
            "claude": {"model": "claude-3-opus"},
            "codex": {"model": "gpt-4"},
            "logging": {"level": "DEBUG"}
        }
        
        settings = Settings(config)
        
        assert settings.claude_config["model"] == "claude-3-opus"
        assert settings.codex_config["model"] == "gpt-4"
        assert settings.logging_config["level"] == "DEBUG"
        
    def test_get_method(self):
        """Test the get method with dot notation."""
        settings = Settings()
        
        assert settings.get("claude.model") == "claude-3-sonnet"
        assert settings.get("codex.model") == "code-davinci-002"
        assert settings.get("nonexistent.key", "default") == "default"
        
    def test_set_method(self):
        """Test the set method with dot notation."""
        settings = Settings()
        
        settings.set("claude.model", "claude-3-haiku")
        assert settings.get("claude.model") == "claude-3-haiku"
        
        settings.set("new.nested.key", "value")
        assert settings.get("new.nested.key") == "value"
        
    def test_environment_variables(self):
        """Test loading configuration from environment variables."""
        with patch.dict(os.environ, {
            'CLAUDE_API_KEY': 'test-claude-key',
            'OPENAI_API_KEY': 'test-openai-key',
            'LOG_LEVEL': 'DEBUG'
        }):
            settings = Settings()
            
            assert settings.claude_config["api_key"] == "test-claude-key"
            assert settings.codex_config["api_key"] == "test-openai-key"
            assert settings.logging_config["level"] == "DEBUG"
            
    def test_config_file_loading(self):
        """Test loading configuration from YAML file."""
        config_content = """
claude:
  api_key: "file-claude-key"
  model: "claude-3-opus"
codex:
  api_key: "file-openai-key"
  model: "gpt-4"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            config_file = f.name
            
        try:
            # Mock the config file paths to include our test file
            with patch('os.path.exists') as mock_exists:
                mock_exists.side_effect = lambda path: path == config_file
                
                with patch('builtins.open', mock_open(read_data=config_content)):
                    with patch('codex_claude_crosstalk.config.settings.Settings._load_config_file') as mock_load:
                        def mock_load_impl(self):
                            with open(config_file, 'r') as f:
                                file_config = yaml.safe_load(f)
                                if file_config:
                                    self._merge_config(self._config, file_config)
                        
                        mock_load.side_effect = mock_load_impl
                        
                        settings = Settings()
                        
                        assert settings.claude_config["api_key"] == "file-claude-key"
                        assert settings.claude_config["model"] == "claude-3-opus"
                        assert settings.codex_config["api_key"] == "file-openai-key"
                        assert settings.codex_config["model"] == "gpt-4"
        finally:
            os.unlink(config_file)
            
    def test_to_dict(self):
        """Test converting settings to dictionary."""
        config = {
            "claude": {"model": "claude-3-opus"},
            "test_key": "test_value"
        }
        
        settings = Settings(config)
        result = settings.to_dict()
        
        assert isinstance(result, dict)
        assert result["claude"]["model"] == "claude-3-opus"
        assert result["test_key"] == "test_value"
        
    def test_save_to_file(self):
        """Test saving configuration to file."""
        settings = Settings()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            test_file = f.name
            
        try:
            settings.save_to_file(test_file)
            
            # Verify the file was created and contains valid YAML
            with open(test_file, 'r') as f:
                loaded_config = yaml.safe_load(f)
                
            assert isinstance(loaded_config, dict)
            assert "claude" in loaded_config
            assert "codex" in loaded_config
        finally:
            os.unlink(test_file)
            
    def test_merge_config(self):
        """Test the config merging functionality."""
        settings = Settings()
        
        base_config = {
            "section1": {
                "key1": "value1",
                "key2": "value2"
            },
            "section2": "value3"
        }
        
        update_config = {
            "section1": {
                "key2": "new_value2",
                "key3": "value4"
            },
            "section3": "value5"
        }
        
        settings._merge_config(base_config, update_config)
        
        assert base_config["section1"]["key1"] == "value1"  # Unchanged
        assert base_config["section1"]["key2"] == "new_value2"  # Updated
        assert base_config["section1"]["key3"] == "value4"  # Added
        assert base_config["section2"] == "value3"  # Unchanged
        assert base_config["section3"] == "value5"  # Added