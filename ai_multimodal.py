"""
Multi-modal AI capabilities for text, vision/image, and audio processing.

This module provides advanced AI capabilities including:
- Text generation with multiple models
- Vision/image analysis and understanding
- Audio transcription and processing
- Model selection and management
- Fine-tuning configuration
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ModelType(str, Enum):
    """Supported AI model types"""
    TEXT = "text"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"


class AIModel:
    """
    Represents an AI model with its capabilities and configuration.
    """
    
    def __init__(
        self,
        model_id: str,
        name: str,
        model_type: ModelType,
        description: str,
        max_tokens: int = 4096,
        supports_streaming: bool = True,
        supports_fine_tuning: bool = False
    ):
        self.model_id = model_id
        self.name = name
        self.model_type = model_type
        self.description = description
        self.max_tokens = max_tokens
        self.supports_streaming = supports_streaming
        self.supports_fine_tuning = supports_fine_tuning
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation"""
        return {
            "model_id": self.model_id,
            "name": self.name,
            "type": self.model_type.value,
            "description": self.description,
            "max_tokens": self.max_tokens,
            "supports_streaming": self.supports_streaming,
            "supports_fine_tuning": self.supports_fine_tuning
        }


class ModelRegistry:
    """
    Registry of available AI models with selection and management capabilities.
    """
    
    def __init__(self):
        self.models: Dict[str, AIModel] = {}
        self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize default OpenAI models"""
        # Text models
        self.register_model(AIModel(
            model_id="gpt-3.5-turbo",
            name="GPT-3.5 Turbo",
            model_type=ModelType.TEXT,
            description="Fast and efficient model for general text tasks",
            max_tokens=4096,
            supports_streaming=True,
            supports_fine_tuning=True
        ))
        
        self.register_model(AIModel(
            model_id="gpt-4",
            name="GPT-4",
            model_type=ModelType.TEXT,
            description="Most capable model for complex reasoning tasks",
            max_tokens=8192,
            supports_streaming=True,
            supports_fine_tuning=False
        ))
        
        self.register_model(AIModel(
            model_id="gpt-4-turbo",
            name="GPT-4 Turbo",
            model_type=ModelType.TEXT,
            description="Enhanced GPT-4 with improved performance and lower cost",
            max_tokens=128000,
            supports_streaming=True,
            supports_fine_tuning=False
        ))
        
        # Vision models
        self.register_model(AIModel(
            model_id="gpt-4-vision-preview",
            name="GPT-4 Vision",
            model_type=ModelType.VISION,
            description="Advanced model for image understanding and analysis",
            max_tokens=4096,
            supports_streaming=False,
            supports_fine_tuning=False
        ))
        
        # Audio models
        self.register_model(AIModel(
            model_id="whisper-1",
            name="Whisper",
            model_type=ModelType.AUDIO,
            description="Speech recognition and transcription model",
            max_tokens=0,  # Audio models don't use token limits
            supports_streaming=False,
            supports_fine_tuning=False
        ))
        
        # Multimodal models
        self.register_model(AIModel(
            model_id="gpt-4o",
            name="GPT-4 Omni",
            model_type=ModelType.MULTIMODAL,
            description="Multimodal model supporting text, vision, and audio",
            max_tokens=128000,
            supports_streaming=True,
            supports_fine_tuning=False
        ))
    
    def register_model(self, model: AIModel) -> bool:
        """
        Register a new model in the registry.
        
        Args:
            model: AIModel instance to register
            
        Returns:
            True if registration successful
        """
        self.models[model.model_id] = model
        logger.info(f"Registered model: {model.name} ({model.model_id})")
        return True
    
    def get_model(self, model_id: str) -> Optional[AIModel]:
        """
        Get a model by its ID.
        
        Args:
            model_id: Model identifier
            
        Returns:
            AIModel instance or None if not found
        """
        return self.models.get(model_id)
    
    def list_models(
        self,
        model_type: Optional[ModelType] = None,
        supports_streaming: Optional[bool] = None,
        supports_fine_tuning: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        List all models with optional filtering.
        
        Args:
            model_type: Filter by model type
            supports_streaming: Filter by streaming support
            supports_fine_tuning: Filter by fine-tuning support
            
        Returns:
            List of model dictionaries
        """
        models = list(self.models.values())
        
        # Apply filters
        if model_type is not None:
            models = [m for m in models if m.model_type == model_type]
        
        if supports_streaming is not None:
            models = [m for m in models if m.supports_streaming == supports_streaming]
        
        if supports_fine_tuning is not None:
            models = [m for m in models if m.supports_fine_tuning == supports_fine_tuning]
        
        return [m.to_dict() for m in models]
    
    def get_models_by_type(self, model_type: ModelType) -> List[Dict[str, Any]]:
        """Get all models of a specific type"""
        return self.list_models(model_type=model_type)


class MultiModalProcessor:
    """
    Process multi-modal AI requests including text, vision, and audio.
    """
    
    def __init__(self, openai_client):
        """
        Initialize the multi-modal processor.
        
        Args:
            openai_client: OpenAI client instance
        """
        self.client = openai_client
        self.model_registry = ModelRegistry()
    
    def process_text(
        self,
        prompt: str,
        model_id: str = "gpt-3.5-turbo",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process text-only requests.
        
        Args:
            prompt: Text prompt
            model_id: Model to use
            **kwargs: Additional parameters
            
        Returns:
            Processing result
        """
        model = self.model_registry.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        if model.model_type not in [ModelType.TEXT, ModelType.MULTIMODAL]:
            raise ValueError(f"Model {model_id} does not support text processing")
        
        return {
            "status": "ready",
            "model_id": model_id,
            "model_type": model.model_type.value,
            "message": "Text processing configured"
        }
    
    def process_vision(
        self,
        prompt: str,
        image_url: str,
        model_id: str = "gpt-4-vision-preview",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process vision/image analysis requests.
        
        Args:
            prompt: Text prompt describing what to analyze
            image_url: URL of the image to analyze
            model_id: Model to use
            **kwargs: Additional parameters
            
        Returns:
            Processing result
        """
        model = self.model_registry.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        if model.model_type not in [ModelType.VISION, ModelType.MULTIMODAL]:
            raise ValueError(f"Model {model_id} does not support vision processing")
        
        return {
            "status": "ready",
            "model_id": model_id,
            "model_type": model.model_type.value,
            "image_url": image_url,
            "message": "Vision processing configured"
        }
    
    def process_audio(
        self,
        audio_url: str,
        model_id: str = "whisper-1",
        language: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process audio transcription requests.
        
        Args:
            audio_url: URL of the audio file
            model_id: Model to use
            language: Optional language code
            **kwargs: Additional parameters
            
        Returns:
            Processing result
        """
        model = self.model_registry.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        if model.model_type not in [ModelType.AUDIO, ModelType.MULTIMODAL]:
            raise ValueError(f"Model {model_id} does not support audio processing")
        
        return {
            "status": "ready",
            "model_id": model_id,
            "model_type": model.model_type.value,
            "audio_url": audio_url,
            "language": language,
            "message": "Audio processing configured"
        }
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific model"""
        model = self.model_registry.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        return model.to_dict()
    
    def list_available_models(
        self,
        model_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all available models with optional type filtering.
        
        Args:
            model_type: Optional model type filter (text, vision, audio, multimodal)
            
        Returns:
            List of available models
        """
        if model_type:
            try:
                mt = ModelType(model_type)
                return self.model_registry.list_models(model_type=mt)
            except ValueError:
                raise ValueError(f"Invalid model type: {model_type}")
        
        return self.model_registry.list_models()


class FineTuningConfig:
    """
    Configuration for model fine-tuning.
    """
    
    def __init__(
        self,
        model_id: str,
        training_file: str,
        validation_file: Optional[str] = None,
        n_epochs: int = 3,
        batch_size: Optional[int] = None,
        learning_rate_multiplier: Optional[float] = None,
        suffix: Optional[str] = None
    ):
        """
        Initialize fine-tuning configuration.
        
        Args:
            model_id: Base model to fine-tune
            training_file: Training data file ID
            validation_file: Optional validation data file ID
            n_epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate_multiplier: Learning rate multiplier
            suffix: Custom suffix for fine-tuned model name
        """
        self.model_id = model_id
        self.training_file = training_file
        self.validation_file = validation_file
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.learning_rate_multiplier = learning_rate_multiplier
        self.suffix = suffix
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        config = {
            "model": self.model_id,
            "training_file": self.training_file,
            "n_epochs": self.n_epochs
        }
        
        if self.validation_file:
            config["validation_file"] = self.validation_file
        if self.batch_size:
            config["batch_size"] = self.batch_size
        if self.learning_rate_multiplier:
            config["learning_rate_multiplier"] = self.learning_rate_multiplier
        if self.suffix:
            config["suffix"] = self.suffix
        
        return config
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate the configuration.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.model_id:
            return False, "model_id is required"
        
        if not self.training_file:
            return False, "training_file is required"
        
        if self.n_epochs < 1 or self.n_epochs > 50:
            return False, "n_epochs must be between 1 and 50"
        
        if self.batch_size is not None and (self.batch_size < 1 or self.batch_size > 256):
            return False, "batch_size must be between 1 and 256"
        
        if self.learning_rate_multiplier is not None:
            if self.learning_rate_multiplier <= 0 or self.learning_rate_multiplier > 10:
                return False, "learning_rate_multiplier must be between 0 and 10"
        
        return True, None


# Global model registry instance
model_registry = ModelRegistry()
