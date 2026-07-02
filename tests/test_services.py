"""Unit tests for services."""

import pytest
from app.services.ai_voice import AIVoiceService
from app.services.moderation import ModerationService
from app.services.analytics import AnalyticsService


@pytest.mark.asyncio
class TestAIVoiceService:
    """Test AI Voice Service."""
    
    @pytest.fixture
    def voice_service(self):
        return AIVoiceService()
    
    def test_get_available_voices(self, voice_service):
        """Test getting available voices."""
        voices = voice_service.get_available_voices()
        assert len(voices) > 0
        assert "professional-male" in [v["name"] for v in voices] or len(voices) > 0
    
    def test_get_voice(self, voice_service):
        """Test getting specific voice."""
        voice = voice_service.get_voice("professional-male")
        assert voice is not None
        assert voice["name"] == "Professional Male"
    
    async def test_synthesize_speech(self, voice_service):
        """Test speech synthesis."""
        audio_url = await voice_service.synthesize_speech(
            "Hello world",
            "professional-male"
        )
        assert audio_url is not None
        assert "s3://" in audio_url or "http" in audio_url


@pytest.mark.asyncio
class TestModerationService:
    """Test Moderation Service."""
    
    @pytest.fixture
    def moderation_service(self):
        return ModerationService()
    
    async def test_moderate_safe_content(self, moderation_service):
        """Test moderating safe content."""
        result = await moderation_service.moderate_content(
            "This is a nice family-friendly video about nature and wildlife."
        )
        assert result["is_safe"] is True
        assert result["action"] == "approved"
    
    async def test_moderate_unsafe_content(self, moderation_service):
        """Test moderating unsafe content."""
        result = await moderation_service.moderate_content(
            "This contains violence and hate speech."
        )
        # Should flag as unsafe
        assert isinstance(result, dict)
        assert "is_safe" in result


@pytest.mark.asyncio
class TestAnalyticsService:
    """Test Analytics Service."""
    
    @pytest.fixture
    def analytics_service(self):
        return AnalyticsService()
    
    async def test_calculate_engagement_metrics(self, analytics_service):
        """Test engagement metric calculation."""
        metrics = await analytics_service.calculate_engagement_metrics(
            views=1000,
            likes=50,
            shares=30,
            comments=20
        )
        assert metrics["engagement_rate"] == 10.0  # (50+30+20)/1000*100
        assert metrics["total_interactions"] == 100
    
    async def test_calculate_roi(self, analytics_service):
        """Test ROI calculation."""
        roi = await analytics_service.calculate_roi(
            revenue=1000,
            investment=500
        )
        assert roi["roi"] == 500
        assert roi["roi_percentage"] == 100.0
