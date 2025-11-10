"""
AI-powered text summarization and analysis tools.

This module provides advanced text processing capabilities including:
- Text summarization with configurable length
- Key points extraction
- Topic identification
"""

from typing import Dict, Any, Optional, List
from openai import OpenAI
import os


class Summarizer:
    """
    AI-powered text summarization using OpenAI models.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the summarizer.
        
        Args:
            model_name: OpenAI model to use for summarization
        """
        self.model_name = model_name
        self.client = None
        
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def summarize(
        self,
        text: str,
        max_length: int = 128,
        style: str = "concise"
    ) -> Dict[str, Any]:
        """
        Summarize the given text.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary in words
            style: Summarization style (concise, detailed, bullet_points)
        
        Returns:
            Dictionary containing summary and metadata
        """
        if not text or not text.strip():
            return {
                "summary": None,
                "status": "error",
                "error": "Input text cannot be empty",
                "input_length": 0
            }
        
        if not self.client:
            return {
                "summary": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured",
                "input_length": len(text)
            }
        
        try:
            # Create appropriate prompt based on style
            if style == "bullet_points":
                prompt = f"Summarize the following text as bullet points (max {max_length} words):\n\n{text}"
            elif style == "detailed":
                prompt = f"Provide a detailed summary of the following text (max {max_length} words):\n\n{text}"
            else:  # concise
                prompt = f"Provide a concise summary of the following text (max {max_length} words):\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at summarizing text concisely and accurately."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_length * 2,  # Rough token estimate
                temperature=0.3  # Lower temperature for more focused summaries
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                "summary": summary,
                "status": "success",
                "input_length": len(text),
                "summary_length": len(summary),
                "style": style,
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "summary": None,
                "status": "error",
                "error": str(e),
                "input_length": len(text)
            }
    
    def extract_key_points(
        self,
        text: str,
        num_points: int = 5
    ) -> Dict[str, Any]:
        """
        Extract key points from the text.
        
        Args:
            text: Text to analyze
            num_points: Number of key points to extract
        
        Returns:
            Dictionary containing key points and metadata
        """
        if not text or not text.strip():
            return {
                "key_points": [],
                "status": "error",
                "error": "Input text cannot be empty"
            }
        
        if not self.client:
            return {
                "key_points": [],
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"Extract the {num_points} most important key points from the following text. Return them as a numbered list:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying key information in text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            key_points_text = response.choices[0].message.content.strip()
            
            # Parse numbered list into array
            lines = key_points_text.split('\n')
            key_points = [line.strip() for line in lines if line.strip()]
            
            return {
                "key_points": key_points,
                "status": "success",
                "count": len(key_points),
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "key_points": [],
                "status": "error",
                "error": str(e)
            }
    
    def identify_topics(
        self,
        text: str,
        max_topics: int = 5
    ) -> Dict[str, Any]:
        """
        Identify main topics in the text.
        
        Args:
            text: Text to analyze
            max_topics: Maximum number of topics to identify
        
        Returns:
            Dictionary containing identified topics
        """
        if not text or not text.strip():
            return {
                "topics": [],
                "status": "error",
                "error": "Input text cannot be empty"
            }
        
        if not self.client:
            return {
                "topics": [],
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            prompt = f"Identify the main topics (up to {max_topics}) discussed in the following text. Return only the topic names as a comma-separated list:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at topic identification and categorization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            topics_text = response.choices[0].message.content.strip()
            topics = [topic.strip() for topic in topics_text.split(',')]
            
            return {
                "topics": topics,
                "status": "success",
                "count": len(topics),
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "topics": [],
                "status": "error",
                "error": str(e)
            }


# Example usage instance
summarizer = Summarizer()

