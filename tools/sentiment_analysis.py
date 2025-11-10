"""
AI-powered sentiment analysis tool.

Analyzes text to determine sentiment, emotions, and tone.
"""

from typing import Dict, Any, Optional, List
from openai import OpenAI
import os


class SentimentAnalyzer:
    """
    AI-powered sentiment analysis using OpenAI models.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the sentiment analyzer.
        
        Args:
            model_name: OpenAI model to use for analysis
        """
        self.model_name = model_name
        self.client = None
        
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
    
    def analyze_sentiment(
        self,
        text: str,
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze the sentiment of the given text.
        
        Args:
            text: Text to analyze
            detailed: If True, provides detailed emotion breakdown
        
        Returns:
            Dictionary containing sentiment analysis results
        """
        if not text or not text.strip():
            return {
                "sentiment": None,
                "status": "error",
                "error": "Input text cannot be empty"
            }
        
        if not self.client:
            return {
                "sentiment": None,
                "status": "not_configured",
                "error": "OpenAI API key not configured"
            }
        
        try:
            if detailed:
                prompt = f"""Analyze the sentiment and emotions in the following text. Provide:
1. Overall sentiment (positive, negative, neutral)
2. Sentiment score (0-100, where 0 is very negative and 100 is very positive)
3. Primary emotions detected (e.g., joy, anger, sadness, fear, surprise)
4. Tone (e.g., formal, casual, aggressive, friendly)

Text: {text}

Return the analysis in this exact format:
Sentiment: [sentiment]
Score: [score]
Emotions: [emotion1, emotion2, ...]
Tone: [tone]"""
            else:
                prompt = f"""Analyze the sentiment of the following text and respond with:
1. Sentiment: positive, negative, or neutral
2. Score: 0-100 (0=very negative, 100=very positive)

Text: {text}

Return only:
Sentiment: [sentiment]
Score: [score]"""
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at sentiment analysis and emotional intelligence."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Parse the response
            result = self._parse_analysis(analysis_text, detailed)
            result["status"] = "success"
            result["model"] = self.model_name
            result["input_length"] = len(text)
            
            return result
        
        except Exception as e:
            return {
                "sentiment": None,
                "status": "error",
                "error": str(e)
            }
    
    def _parse_analysis(
        self,
        analysis_text: str,
        detailed: bool
    ) -> Dict[str, Any]:
        """Parse the analysis response from the AI."""
        result = {}
        
        lines = analysis_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Sentiment:'):
                result['sentiment'] = line.split(':', 1)[1].strip().lower()
            elif line.startswith('Score:'):
                try:
                    score_text = line.split(':', 1)[1].strip()
                    result['score'] = int(score_text.split()[0])
                except:
                    result['score'] = None
            elif detailed and line.startswith('Emotions:'):
                emotions_text = line.split(':', 1)[1].strip()
                result['emotions'] = [e.strip() for e in emotions_text.split(',')]
            elif detailed and line.startswith('Tone:'):
                result['tone'] = line.split(':', 1)[1].strip()
        
        return result
    
    def batch_analyze(
        self,
        texts: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
        
        Returns:
            Dictionary containing batch analysis results
        """
        if not texts:
            return {
                "results": [],
                "status": "error",
                "error": "No texts provided"
            }
        
        results = []
        for i, text in enumerate(texts):
            analysis = self.analyze_sentiment(text, detailed=False)
            analysis['index'] = i
            results.append(analysis)
        
        # Calculate aggregate statistics
        successful = [r for r in results if r.get('status') == 'success']
        if successful:
            avg_score = sum(r.get('score', 0) for r in successful) / len(successful)
            sentiment_counts = {}
            for r in successful:
                sentiment = r.get('sentiment', 'unknown')
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        else:
            avg_score = None
            sentiment_counts = {}
        
        return {
            "results": results,
            "status": "success",
            "total_analyzed": len(texts),
            "successful": len(successful),
            "average_score": avg_score,
            "sentiment_distribution": sentiment_counts
        }
    
    def compare_sentiment(
        self,
        text1: str,
        text2: str
    ) -> Dict[str, Any]:
        """
        Compare sentiment between two texts.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Dictionary containing comparison results
        """
        analysis1 = self.analyze_sentiment(text1, detailed=False)
        analysis2 = self.analyze_sentiment(text2, detailed=False)
        
        if analysis1['status'] == 'success' and analysis2['status'] == 'success':
            score_diff = analysis1.get('score', 0) - analysis2.get('score', 0)
            
            return {
                "status": "success",
                "text1": {
                    "sentiment": analysis1.get('sentiment'),
                    "score": analysis1.get('score')
                },
                "text2": {
                    "sentiment": analysis2.get('sentiment'),
                    "score": analysis2.get('score')
                },
                "difference": {
                    "score_diff": score_diff,
                    "interpretation": self._interpret_difference(score_diff)
                }
            }
        else:
            return {
                "status": "error",
                "error": "Failed to analyze one or both texts",
                "text1": analysis1,
                "text2": analysis2
            }
    
    def _interpret_difference(self, score_diff: float) -> str:
        """Interpret the sentiment score difference."""
        if abs(score_diff) < 10:
            return "very similar sentiment"
        elif abs(score_diff) < 25:
            return "slightly different sentiment"
        elif abs(score_diff) < 50:
            return "moderately different sentiment"
        else:
            return "very different sentiment"


# Example usage instance
sentiment_analyzer = SentimentAnalyzer()
