# ai_capabilities.py
# Expanded model, multi-modal support, and fine-tuning capabilities

from typing import List, Dict, Optional, Union
from enum import Enum


class ModelType(Enum):
    """Supported AI model types"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    MULTI_MODAL = "multi-modal"


class SupportedModel(Enum):
    """Supported AI models with their capabilities"""
    # Text models
    GPT_4 = ("gpt-4", [ModelType.TEXT])
    GPT_4_TURBO = ("gpt-4-turbo-preview", [ModelType.TEXT])
    GPT_35_TURBO = ("gpt-3.5-turbo", [ModelType.TEXT])
    
    # Vision models
    GPT_4_VISION = ("gpt-4-vision-preview", [ModelType.TEXT, ModelType.IMAGE])
    
    # Audio models
    WHISPER = ("whisper-1", [ModelType.AUDIO])
    TTS_1 = ("tts-1", [ModelType.TEXT, ModelType.AUDIO])
    TTS_1_HD = ("tts-1-hd", [ModelType.TEXT, ModelType.AUDIO])
    
    # Image generation models
    DALL_E_3 = ("dall-e-3", [ModelType.TEXT, ModelType.IMAGE])
    DALL_E_2 = ("dall-e-2", [ModelType.TEXT, ModelType.IMAGE])
    
    def __init__(self, model_name: str, capabilities: List[ModelType]):
        self.model_name = model_name
        self.capabilities = capabilities


class FineTuningConfig:
    """Configuration for fine-tuning AI models"""
    
    def __init__(
        self,
        training_file: str,
        model: str = "gpt-3.5-turbo",
        validation_file: Optional[str] = None,
        hyperparameters: Optional[Dict] = None,
        suffix: Optional[str] = None
    ):
        self.training_file = training_file
        self.model = model
        self.validation_file = validation_file
        self.hyperparameters = hyperparameters or {
            "n_epochs": 3,
            "batch_size": "auto",
            "learning_rate_multiplier": "auto"
        }
        self.suffix = suffix
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary"""
        config = {
            "training_file": self.training_file,
            "model": self.model,
            "hyperparameters": self.hyperparameters
        }
        if self.validation_file:
            config["validation_file"] = self.validation_file
        if self.suffix:
            config["suffix"] = self.suffix
        return config


class AICapability:
    """Enhanced AI capability class with multi-modal support"""
    
    def __init__(self, model_name: str, modes: List[str]):
        self.model_name = model_name
        self.modes = modes  # e.g. ['text', 'image', 'audio']
        self.supported_models = self._get_supported_models()
    
    def _get_supported_models(self) -> Dict[str, SupportedModel]:
        """Get dictionary of supported models"""
        return {model.model_name: model for model in SupportedModel}
    
    def analyze_text(self, input_data: str, **kwargs) -> Dict:
        """
        Process text input using AI models
        
        Args:
            input_data: Text to analyze
            **kwargs: Additional parameters for the model
            
        Returns:
            Dictionary with analysis results
        """
        return {
            'input_type': 'text',
            'model': self.model_name,
            'output': None,
            'status': 'ready',
            'message': 'Text processing ready - use API endpoints for actual processing'
        }
    
    def analyze_image(self, input_data: Union[str, bytes], prompt: Optional[str] = None, **kwargs) -> Dict:
        """
        Process image input using vision models
        
        Args:
            input_data: Image URL or image bytes
            prompt: Optional text prompt for image analysis
            **kwargs: Additional parameters for the model
            
        Returns:
            Dictionary with analysis results
        """
        return {
            'input_type': 'image',
            'model': self.model_name,
            'prompt': prompt,
            'output': None,
            'status': 'ready',
            'message': 'Image processing ready - use API endpoints for actual processing'
        }
    
    def analyze_audio(self, input_data: Union[str, bytes], **kwargs) -> Dict:
        """
        Process audio input using audio models (e.g., Whisper for transcription)
        
        Args:
            input_data: Audio file path or audio bytes
            **kwargs: Additional parameters for the model
            
        Returns:
            Dictionary with analysis results (transcription, etc.)
        """
        return {
            'input_type': 'audio',
            'model': self.model_name,
            'output': None,
            'status': 'ready',
            'message': 'Audio processing ready - use API endpoints for actual processing'
        }
    
    def analyze(self, input_data: Union[str, bytes, Dict], input_type: Optional[str] = None, **kwargs) -> Dict:
        """
        Multi-modal processing - automatically detects or uses specified input type
        
        Args:
            input_data: Input data of any supported type
            input_type: Optional type specification ('text', 'image', 'audio')
            **kwargs: Additional parameters for the model
            
        Returns:
            Dictionary with processing results
        """
        if input_type == 'text' or (isinstance(input_data, str) and input_type is None):
            return self.analyze_text(input_data, **kwargs)
        elif input_type == 'image':
            return self.analyze_image(input_data, **kwargs)
        elif input_type == 'audio':
            return self.analyze_audio(input_data, **kwargs)
        else:
            return {
                'output': None,
                'status': 'error',
                'message': 'Unable to determine input type'
            }
    
    def fine_tune(self, config: FineTuningConfig) -> Dict:
        """
        Configure fine-tuning for AI models
        
        Args:
            config: FineTuningConfig object with training parameters
            
        Returns:
            Dictionary with fine-tuning configuration status
        """
        return {
            'model': config.model,
            'training_file': config.training_file,
            'hyperparameters': config.hyperparameters,
            'status': 'configured',
            'message': 'Fine-tuning configuration ready - use API endpoints to start fine-tuning'
        }
    
    def get_model_info(self, model_name: Optional[str] = None) -> Dict:
        """
        Get information about supported models
        
        Args:
            model_name: Optional specific model name to query
            
        Returns:
            Dictionary with model information
        """
        if model_name:
            if model_name in self.supported_models:
                model = self.supported_models[model_name]
                return {
                    'model_name': model.model_name,
                    'capabilities': [cap.value for cap in model.capabilities],
                    'status': 'available'
                }
            else:
                return {
                    'model_name': model_name,
                    'status': 'not_found'
                }
        else:
            return {
                'supported_models': [
                    {
                        'model_name': model.model_name,
                        'capabilities': [cap.value for cap in model.capabilities]
                    }
                    for model in SupportedModel
                ],
                'total_count': len(SupportedModel)
            }


# Example instances with different capabilities
text_capability = AICapability('gpt-3.5-turbo', ['text'])
vision_capability = AICapability('gpt-4-vision-preview', ['text', 'image'])
audio_capability = AICapability('whisper-1', ['audio'])
multi_modal_capability = AICapability('gpt-4-vision-preview', ['text', 'image', 'audio'])
