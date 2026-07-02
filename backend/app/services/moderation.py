"""Content moderation service."""

import logging
from typing import Dict, List, Tuple
import asyncio

logger = logging.getLogger(__name__)


class ModerationService:
    """Service for content moderation and safety."""
    
    def __init__(self):
        self.blocked_keywords = self._load_blocked_keywords()
        self.blocked_patterns = self._load_blocked_patterns()
    
    def _load_blocked_keywords(self) -> List[str]:
        """Load blocked keywords for moderation."""
        return [
            "violence", "hate", "abuse", "spam",
            "explicit", "illegal", "harassment"
        ]
    
    def _load_blocked_patterns(self) -> List[str]:
        """Load regex patterns for blocked content."""
        return []
    
    async def moderate_content(
        self,
        content: str,
        content_type: str = "text"
    ) -> Dict:
        """Moderate content for policy violations."""
        logger.info(f"Moderating {content_type} content")
        
        try:
            # Check for blocked keywords
            violations = await self._check_blocked_keywords(content)
            
            # Check for patterns
            if not violations:
                violations = await self._check_patterns(content)
            
            is_safe = len(violations) == 0
            
            return {
                "is_safe": is_safe,
                "violations": violations,
                "confidence_score": 0.95 if is_safe else 0.75,
                "action": "approved" if is_safe else "flagged_for_review"
            }
        except Exception as e:
            logger.error(f"Error moderating content: {str(e)}")
            return {
                "is_safe": False,
                "violations": ["moderation_error"],
                "confidence_score": 0.0,
                "action": "rejected"
            }
    
    async def _check_blocked_keywords(self, content: str) -> List[str]:
        """Check for blocked keywords in content."""
        await asyncio.sleep(0.05)  # Simulate processing
        
        violations = []
        content_lower = content.lower()
        
        for keyword in self.blocked_keywords:
            if keyword in content_lower:
                violations.append(f"blocked_keyword: {keyword}")
        
        return violations
    
    async def _check_patterns(self, content: str) -> List[str]:
        """Check for blocked patterns in content."""
        await asyncio.sleep(0.05)  # Simulate processing
        return []
    
    async def moderate_batch(
        self,
        contents: List[str]
    ) -> List[Dict]:
        """Moderate multiple content pieces."""
        logger.info(f"Moderating batch of {len(contents)} items")
        
        tasks = [self.moderate_content(content) for content in contents]
        return await asyncio.gather(*tasks)
    
    async def flag_for_review(
        self,
        content_id: str,
        reason: str
    ) -> Dict:
        """Flag content for manual review."""
        logger.warning(f"Flagging content {content_id} for review: {reason}")
        
        return {
            "content_id": content_id,
            "reason": reason,
            "status": "pending_review",
            "reviewer_assignment": None
        }
