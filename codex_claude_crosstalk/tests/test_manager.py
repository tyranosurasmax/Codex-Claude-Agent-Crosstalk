"""
Tests for the core CrosstalkManager functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from codex_claude_crosstalk.core.manager import CrosstalkManager
from codex_claude_crosstalk.config.settings import Settings


class TestCrosstalkManager:
    """Test cases for CrosstalkManager."""
    
    def test_initialization(self):
        """Test basic initialization."""
        manager = CrosstalkManager()
        assert manager is not None
        assert not manager._initialized
        assert manager.claude_agent is None
        assert manager.codex_agent is None
        
    def test_initialization_with_config(self):
        """Test initialization with custom config."""
        config = {
            "claude": {"api_key": "test-key"},
            "codex": {"api_key": "test-key"}
        }
        manager = CrosstalkManager(config)
        assert manager.settings.claude_config["api_key"] == "test-key"
        assert manager.settings.codex_config["api_key"] == "test-key"
        
    @pytest.mark.asyncio
    async def test_initialize_agents(self):
        """Test agent initialization."""
        manager = CrosstalkManager()
        
        # Mock the agent classes to avoid actual API calls
        with patch('codex_claude_crosstalk.agents.claude_agent.ClaudeAgent') as mock_claude, \
             patch('codex_claude_crosstalk.agents.codex_agent.CodexAgent') as mock_codex:
            
            # Set up mocks
            mock_claude_instance = Mock()
            mock_codex_instance = Mock()
            mock_claude.return_value = mock_claude_instance
            mock_codex.return_value = mock_codex_instance
            
            # Make initialize methods async
            async def mock_init():
                pass
            
            mock_claude_instance.initialize = mock_init
            mock_codex_instance.initialize = mock_init
            
            await manager.initialize()
            
            assert manager._initialized
            assert manager.claude_agent == mock_claude_instance
            assert manager.codex_agent == mock_codex_instance
            
    @pytest.mark.asyncio
    async def test_generate_project(self):
        """Test project generation."""
        manager = CrosstalkManager()
        
        with patch('codex_claude_crosstalk.agents.claude_agent.ClaudeAgent') as mock_claude, \
             patch('codex_claude_crosstalk.agents.codex_agent.CodexAgent') as mock_codex:
            
            # Set up mocks
            mock_claude_instance = Mock()
            mock_codex_instance = Mock()
            mock_claude.return_value = mock_claude_instance
            mock_codex.return_value = mock_codex_instance
            
            # Mock async methods
            async def mock_init():
                pass
            
            async def mock_design_structure():
                return {
                    "name": "test-project",
                    "type": "cli-tool",
                    "architecture": {"pattern": "Command"},
                    "files": ["main.py"],
                    "dependencies": ["click"]
                }
                
            async def mock_implement():
                return {"files": {"main.py": "# Generated code"}}
                
            async def mock_review():
                return {
                    "files": {"main.py": "# Reviewed code"},
                    "review_notes": ["Good structure"]
                }
            
            mock_claude_instance.initialize = mock_init
            mock_codex_instance.initialize = mock_init
            mock_claude_instance.design_project_structure = mock_design_structure
            mock_codex_instance.implement_project = mock_implement
            mock_claude_instance.review_implementation = mock_review
            
            # Test project generation
            result = await manager.generate_project("test-project", "cli-tool")
            
            assert result["name"] == "test-project"
            assert result["type"] == "cli-tool"
            assert result["status"] == "completed"
            assert "structure" in result
            assert "implementation" in result
            
    @pytest.mark.asyncio
    async def test_generate_component(self):
        """Test component generation."""
        manager = CrosstalkManager()
        
        with patch('codex_claude_crosstalk.agents.claude_agent.ClaudeAgent') as mock_claude, \
             patch('codex_claude_crosstalk.agents.codex_agent.CodexAgent') as mock_codex:
            
            # Set up mocks
            mock_claude_instance = Mock()
            mock_codex_instance = Mock()
            mock_claude.return_value = mock_claude_instance
            mock_codex.return_value = mock_codex_instance
            
            # Mock async methods
            async def mock_init():
                pass
            
            async def mock_generate_component():
                return {
                    "name": "TestComponent",
                    "code": "class TestComponent: pass"
                }
                
            async def mock_review_code():
                return {
                    "name": "TestComponent", 
                    "code": "class TestComponent: pass",
                    "claude_review": {"quality_score": 8.5}
                }
            
            mock_claude_instance.initialize = mock_init
            mock_codex_instance.initialize = mock_init
            mock_codex_instance.generate_component = mock_generate_component
            mock_claude_instance.review_code = mock_review_code
            
            # Test component generation with review
            result = await manager.generate_component("TestComponent", {"type": "class"}, review=True)
            
            assert result["name"] == "TestComponent"
            assert "claude_review" in result
            
            # Test component generation without review
            result = await manager.generate_component("TestComponent", {"type": "class"}, review=False)
            
            assert result["name"] == "TestComponent"
            assert "claude_review" not in result
            
    @pytest.mark.asyncio
    async def test_close(self):
        """Test cleanup."""
        manager = CrosstalkManager()
        
        with patch('codex_claude_crosstalk.agents.claude_agent.ClaudeAgent') as mock_claude, \
             patch('codex_claude_crosstalk.agents.codex_agent.CodexAgent') as mock_codex:
            
            # Set up mocks
            mock_claude_instance = Mock()
            mock_codex_instance = Mock()
            mock_claude.return_value = mock_claude_instance
            mock_codex.return_value = mock_codex_instance
            
            # Mock async methods
            async def mock_init():
                pass
                
            async def mock_close():
                pass
            
            mock_claude_instance.initialize = mock_init
            mock_codex_instance.initialize = mock_init
            mock_claude_instance.close = mock_close
            mock_codex_instance.close = mock_close
            
            await manager.initialize()
            await manager.close()
            
            mock_claude_instance.close.assert_called_once()
            mock_codex_instance.close.assert_called_once()