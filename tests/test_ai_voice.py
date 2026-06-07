import pytest
from unittest.mock import Mock, patch
from backend.app.services.ai_voice import AIVoiceService

class TestAIVoiceService:
    def setup_method(self):
        self.voice_service = AIVoiceService()
    
    def test_generate_speech_success(self):
        """Test successful speech generation"""
        text = "Hello, this is a test message"
        voice = "professional-female"
        
        with patch('backend.app.services.ai_voice.elevenlabs_client') as mock_client:
            mock_response = Mock()
            mock_response.content = b"fake_audio_data"
            mock_client.generate.return_value = mock_response
            
            result = self.voice_service.generate_speech(text, voice)
            
            assert result is not None
            assert len(result) > 0
            mock_client.generate.assert_called_once_with(
                text=text,
                voice=voice,
                model="eleven_monolingual_v1"
            )
    
    def test_generate_speech_invalid_voice(self):
        """Test speech generation with invalid voice"""
        with pytest.raises(ValueError):
            self.voice_service.generate_speech("test", "invalid-voice")
    
    def test_generate_speech_empty_text(self):
        """Test speech generation with empty text"""
        with pytest.raises(ValueError):
            self.voice_service.generate_speech("", "professional-female")
    
    def test_list_available_voices(self):
        """Test listing available voices"""
        voices = self.voice_service.list_available_voices()
        assert isinstance(voices, list)
        assert len(voices) > 0
        assert "professional-female" in voices
        assert "professional-male" in voices
    
    @patch('backend.app.services.ai_voice.elevenlabs_client')
    def test_generate_speech_api_error(self, mock_client):
        """Test handling of API errors"""
        mock_client.generate.side_effect = Exception("API Error")
        
        with pytest.raises(Exception):
            self.voice_service.generate_speech("test", "professional-female")
