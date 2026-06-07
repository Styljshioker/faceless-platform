"""Content Creation Pipeline Service."""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import uuid

from app.services.ai_voice import AIVoiceService
from app.services.video_templates import VideoTemplateService
from app.services.moderation import ModerationService


class ContentStatus(Enum):
    """Content processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ContentRequest:
    """Content creation request."""
    id: str
    user_id: str
    script: str
    template_id: str
    voice_config: Dict
    output_format: str = "mp4"
    status: ContentStatus = ContentStatus.PENDING


class ContentPipeline:
    """Automated content creation pipeline."""
    
    def __init__(self):
        self.voice_service = AIVoiceService()
        self.template_service = VideoTemplateService()
        self.moderation_service = ModerationService()
        self.active_jobs: Dict[str, ContentRequest] = {}
    
    async def create_content(
        self, 
        user_id: str, 
        script: str, 
        template_id: str, 
        voice_config: Dict
    ) -> str:
        """Create new content request."""
        
        # Content moderation
        moderation_result = await self.moderation_service.moderate_text(script)
        if not moderation_result.is_safe:
            raise ValueError(f"Content flagged: {moderation_result.reason}")
        
        # Create job
        job_id = str(uuid.uuid4())
        request = ContentRequest(
            id=job_id,
            user_id=user_id,
            script=script,
            template_id=template_id,
            voice_config=voice_config
        )
        
        self.active_jobs[job_id] = request
        
        # Process asynchronously
        asyncio.create_task(self._process_content(request))
        
        return job_id
    
    async def _process_content(self, request: ContentRequest):
        """Process content creation request."""
        try:
            request.status = ContentStatus.PROCESSING
            
            # Step 1: Generate voice
            audio_file = await self.voice_service.generate_speech(
                text=request.script,
                **request.voice_config
            )
            
            # Step 2: Apply video template
            video_file = await self.template_service.create_video(
                template_id=request.template_id,
                audio_file=audio_file,
                script=request.script
            )
            
            # Step 3: Final processing
            final_video = await self._finalize_video(video_file, request)
            
            request.status = ContentStatus.COMPLETED
            
            # Notify completion (webhook, database update, etc.)
            await self._notify_completion(request, final_video)
            
        except Exception as e:
            request.status = ContentStatus.FAILED
            await self._handle_error(request, str(e))
    
    async def _finalize_video(self, video_file: str, request: ContentRequest) -> str:
        """Final video processing steps."""
        # Add watermark, optimize, upload to storage, etc.
        return video_file
    
    async def _notify_completion(self, request: ContentRequest, video_file: str):
        """Notify user of completion."""
        # Send webhook, email, push notification, etc.
        pass
    
    async def _handle_error(self, request: ContentRequest, error: str):
        """Handle processing errors."""
        # Log error, notify user, cleanup, etc.
        pass
    
    async def get_job_status(self, job_id: str) -> Dict:
        """Get job processing status."""
        if job_id not in self.active_jobs:
            raise ValueError("Job not found")
        
        job = self.active_jobs[job_id]
        return {
            "id": job.id,
            "status": job.status.value,
            "progress": self._calculate_progress(job)
        }
    
    def _calculate_progress(self, job: ContentRequest) -> int:
        """Calculate job progress percentage."""
        status_progress = {
            ContentStatus.PENDING: 0,
            ContentStatus.PROCESSING: 50,
            ContentStatus.COMPLETED: 100,
            ContentStatus.FAILED: 0
        }
        return status_progress.get(job.status, 0)
