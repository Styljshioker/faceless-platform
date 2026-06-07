import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.app.services.content_pipeline import ContentPipelineService

class TestContentPipelineService:
    def setup_method(self):
        self.pipeline_service = ContentPipelineService()
    
    def test_process_script_success(self):
        """Test successful script processing"""
        script_content = "This is a test script for content creation."
        template_id = "modern-tech"
        
        with patch.object(self.pipeline_service, '_validate_script') as mock_validate:
            with patch.object(self.pipeline_service, '_extract_metadata') as mock_metadata:
                mock_validate.return_value = True
                mock_metadata.return_value = {
                    "duration": 30,
                    "word_count": 10,
                    "complexity": "simple"
                }
                
                result = self.pipeline_service.process_script(
                    script_content, template_id
                )
                
                assert result is not None
                assert "content_id" in result
                assert "status" in result
                assert result["status"] == "processed"
    
    def test_process_script_invalid_template(self):
        """Test script processing with invalid template"""
        with pytest.raises(ValueError):
            self.pipeline_service.process_script(
                "test script", "invalid-template"
            )
    
    def test_validate_script_empty(self):
        """Test script validation with empty content"""
        assert not self.pipeline_service._validate_script("")
        assert not self.pipeline_service._validate_script(None)
    
    def test_validate_script_too_long(self):
        """Test script validation with content too long"""
        long_script = "a" * 10001  # Assuming 10000 char limit
        assert not self.pipeline_service._validate_script(long_script)
    
    def test_extract_metadata(self):
        """Test metadata extraction from script"""
        script = "This is a sample script with multiple sentences. " * 5
        metadata = self.pipeline_service._extract_metadata(script)
        
        assert "duration" in metadata
        assert "word_count" in metadata
        assert "complexity" in metadata
        assert metadata["word_count"] > 0
        assert metadata["duration"] > 0
    
    def test_generate_thumbnails(self):
        """Test thumbnail generation"""
        content_data = {
            "title": "Test Video",
            "template": "modern-tech",
            "script": "Test script content"
        }
        
        with patch('backend.app.services.content_pipeline.generate_image') as mock_gen:
            mock_gen.return_value = b"fake_image_data"
            
            thumbnails = self.pipeline_service.generate_thumbnails(content_data)
            
            assert isinstance(thumbnails, list)
            assert len(thumbnails) > 0
    
    @patch('backend.app.services.content_pipeline.ContentPipelineService._save_to_database')
    def test_create_content_success(self, mock_save):
        """Test successful content creation"""
        mock_save.return_value = {"id": "test-content-123"}
        
        content_data = {
            "title": "Test Content",
            "script": "This is test content",
            "template": "modern-tech",
            "voice": "professional-female"
        }
        
        result = self.pipeline_service.create_content(content_data)
        
        assert "id" in result
        assert result["id"] == "test-content-123"
        mock_save.assert_called_once()
