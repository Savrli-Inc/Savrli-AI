"""
Email drafting assistant using AI.

Generates professional email drafts based on context and requirements.
"""

from typing import Dict, Any, Optional, List
from openai import OpenAI
import os


class EmailDrafter:
    """
    AI-powered email drafting assistant.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the email drafter.
        
        Args:
            model_name: OpenAI model to use
        """
        self.model_name = model_name
        self.client = None
        
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def draft_email(
        self,
        purpose: str,
        recipient: Optional[str] = None,
        tone: str = "professional",
        key_points: Optional[List[str]] = None,
        length: str = "medium",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate an email draft.
        
        Args:
            purpose: Purpose of the email (e.g., "follow up on meeting")
            recipient: Optional recipient name or role
            tone: Email tone (professional, casual, friendly, formal)
            key_points: List of key points to include
            length: Email length (short, medium, long)
            context: Additional context or background information
        
        Returns:
            Dictionary containing email draft and metadata
        """
        if not purpose or not purpose.strip():
            return {
                "draft": None,
                "status": "error",
                "error": "Email purpose cannot be empty"
            }
        
        if not self.client:
            return {
                "draft": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            # Build the prompt
            prompt_parts = [f"Draft a {tone} email for the following purpose: {purpose}"]
            
            if recipient:
                prompt_parts.append(f"Recipient: {recipient}")
            
            if key_points:
                prompt_parts.append(f"Key points to include:\n" + "\n".join(f"- {point}" for point in key_points))
            
            if context:
                prompt_parts.append(f"Context: {context}")
            
            length_guidance = {
                "short": "Keep it brief and to the point (2-3 paragraphs)",
                "medium": "Use moderate length (3-4 paragraphs)",
                "long": "Provide comprehensive details (5+ paragraphs)"
            }
            prompt_parts.append(length_guidance.get(length, length_guidance["medium"]))
            
            prompt_parts.append("\nGenerate the email with a subject line in this format:\nSubject: [subject]\n\n[email body]")
            
            prompt = "\n\n".join(prompt_parts)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at writing professional emails. Always include a subject line and well-structured body."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            draft = response.choices[0].message.content.strip()
            
            # Parse subject and body
            subject, body = self._parse_email(draft)
            
            return {
                "draft": draft,
                "subject": subject,
                "body": body,
                "status": "success",
                "model": self.model_name,
                "tone": tone,
                "length": length
            }
        
        except Exception as e:
            return {
                "draft": None,
                "status": "error",
                "error": str(e)
            }
    
    def _parse_email(self, draft: str) -> tuple[Optional[str], Optional[str]]:
        """Parse email into subject and body."""
        lines = draft.split('\n', 1)
        subject = None
        body = None
        
        if len(lines) > 0 and lines[0].strip().startswith('Subject:'):
            subject = lines[0].replace('Subject:', '').strip()
            if len(lines) > 1:
                body = lines[1].strip()
        else:
            body = draft
        
        return subject, body
    
    def improve_email(
        self,
        email_text: str,
        improvements: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Improve an existing email draft.
        
        Args:
            email_text: Original email text
            improvements: Specific improvements to make (e.g., ["make more concise", "add urgency"])
        
        Returns:
            Dictionary containing improved email
        """
        if not email_text or not email_text.strip():
            return {
                "improved_draft": None,
                "status": "error",
                "error": "Email text cannot be empty"
            }
        
        if not self.client:
            return {
                "improved_draft": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"Improve the following email:\n\n{email_text}\n\n"
            
            if improvements:
                prompt += "Specific improvements needed:\n" + "\n".join(f"- {imp}" for imp in improvements)
            else:
                prompt += "Make it more professional, clear, and effective while maintaining the core message."
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at improving email communication."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            improved_draft = response.choices[0].message.content.strip()
            
            return {
                "improved_draft": improved_draft,
                "original_draft": email_text,
                "status": "success",
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "improved_draft": None,
                "status": "error",
                "error": str(e)
            }
    
    def generate_reply(
        self,
        original_email: str,
        reply_purpose: str,
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        Generate a reply to an email.
        
        Args:
            original_email: The email to reply to
            reply_purpose: Purpose of the reply
            tone: Tone of the reply
        
        Returns:
            Dictionary containing reply draft
        """
        if not original_email or not original_email.strip():
            return {
                "reply": None,
                "status": "error",
                "error": "Original email cannot be empty"
            }
        
        if not reply_purpose or not reply_purpose.strip():
            return {
                "reply": None,
                "status": "error",
                "error": "Reply purpose cannot be empty"
            }
        
        if not self.client:
            return {
                "reply": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"""Generate a {tone} reply to the following email:

Original Email:
{original_email}

Reply Purpose: {reply_purpose}

Generate the reply with a subject line (Re: [original subject]) and body."""
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at crafting email replies that are appropriate and effective."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content.strip()
            
            return {
                "reply": reply,
                "status": "success",
                "model": self.model_name,
                "tone": tone
            }
        
        except Exception as e:
            return {
                "reply": None,
                "status": "error",
                "error": str(e)
            }


# Example usage instance
email_drafter = EmailDrafter()
