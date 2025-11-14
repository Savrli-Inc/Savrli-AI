"""
Multimodal Feature Tests

This test suite validates the multimodal capabilities of the Savrli AI API,
including vision/image analysis, audio transcription, image generation,
model listing, and fine-tuning configuration.

Related Issues:
- Issue #32: Multimodal feature implementation
- Issue #36: Advanced features and integrations (saved issue)

Test Coverage:
- Vision endpoint (/ai/vision)
- Audio transcription endpoint (/ai/audio/transcribe)
- Image generation endpoint (/ai/image/generate)
- Models listing endpoint (/ai/models)
- Fine-tuning configuration endpoint (/ai/fine-tune/configure)

Example Request/Response Formats:
-------------------------------------

VISION ENDPOINT:
Request:
    POST /ai/vision
    {
        "prompt": "What's in this image?",
        "image_url": "https://example.com/image.jpg",
        "detail": "high"  // optional: "low", "high", or "auto"
    }
Response:
    {
        "response": "This is a cat sitting on a couch.",
        "model": "gpt-4-vision-preview",
        "input_type": "image",
        "image_url": "https://example.com/image.jpg"
    }

AUDIO TRANSCRIPTION ENDPOINT:
Request:
    POST /ai/audio/transcribe
    Content-Type: multipart/form-data
    file: [audio file]
    language: "en"  // optional
    prompt: "Context for transcription"  // optional
Response:
    {
        "transcription": "This is the transcribed text.",
        "model": "whisper-1",
        "input_type": "audio"
    }

IMAGE GENERATION ENDPOINT:
Request:
    POST /ai/image/generate
    {
        "prompt": "A beautiful sunset over mountains",
        "model": "dall-e-3",  // optional: "dall-e-2" or "dall-e-3"
        "size": "1024x1024",  // optional, varies by model
        "quality": "hd",      // optional: "standard" or "hd" (DALL-E 3 only)
        "n": 1                // optional: number of images (1-10 for DALL-E 2)
    }
Response:
    {
        "images": [
            {
                "url": "https://example.com/generated_image.png",
                "revised_prompt": "A detailed version of the prompt"
            }
        ],
        "model": "dall-e-3",
        "prompt": "A beautiful sunset over mountains"
    }

MODELS LISTING ENDPOINT:
Request:
    GET /ai/models
Response:
    {
        "models": [
            {
                "model_id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "type": "text",
                "description": "Fast and efficient model",
                "max_tokens": 4096,
                "supports_streaming": true,
                "supports_fine_tuning": true
            },
            ...
        ],
        "total_count": 6,
        "capabilities": {
            "text": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "image_analysis": ["gpt-4-vision-preview", "gpt-4o"],
            "image_generation": ["dall-e-2", "dall-e-3"],
            "audio": ["whisper-1"]
        }
    }

FINE-TUNING CONFIGURATION:
Request:
    POST /ai/fine-tune/configure
    {
        "training_file": "file-abc123",
        "validation_file": "file-xyz789",  // optional
        "model": "gpt-3.5-turbo",
        "n_epochs": 5,
        "batch_size": "4",                 // optional
        "learning_rate_multiplier": "0.1", // optional
        "suffix": "custom-model"           // optional
    }
Response:
    {
        "status": "configured",
        "configuration": {
            "training_file": "file-abc123",
            "validation_file": "file-xyz789",
            "model": "gpt-3.5-turbo",
            "suffix": "custom-model",
            "hyperparameters": {
                "n_epochs": 5,
                "batch_size": "4",
                "learning_rate_multiplier": "0.1"
            }
        }
    }
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
import os
import sys
import io
import base64

# Add parent directory to path to import the API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app

client = TestClient(app)


class TestVisionEndpoint:
    """Test vision/image analysis endpoint
    
    TODO (Issue #32): Ensure response includes 'input_type' field
    TODO (Issue #32): Verify image_url is returned in response
    """
    
    @patch('api.index.client.chat.completions.create')
    def test_vision_with_url(self, mock_create):
        """Test vision endpoint with image URL"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a cat sitting on a couch."
        mock_create.return_value = mock_response
        
        response = client.post("/ai/vision", json={
            "prompt": "What's in this image?",
            "image_url": "https://example.com/image.jpg"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["model"] == "gpt-4-vision-preview"
        # TODO (Issue #32): Fix endpoint to return input_type field
        assert data["input_type"] == "image"
    
    @patch('api.index.client.chat.completions.create')
    def test_vision_with_base64(self, mock_create):
        """Test vision endpoint with base64 image"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Image analysis result"
        mock_create.return_value = mock_response
        
        # Create a simple base64 string
        image_base64 = base64.b64encode(b"fake image data").decode()
        
        response = client.post("/ai/vision", json={
            "prompt": "Describe this image",
            "image_base64": image_base64
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
    
    def test_vision_no_image(self):
        """Test that vision endpoint requires an image"""
        response = client.post("/ai/vision", json={
            "prompt": "What's in this image?"
        })
        
        assert response.status_code == 400
        assert "image_url or image_base64" in response.json()["detail"]
    
    def test_vision_empty_prompt(self):
        """Test that vision endpoint requires a prompt"""
        response = client.post("/ai/vision", json={
            "prompt": "",
            "image_url": "https://example.com/image.jpg"
        })
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    @patch('api.index.client.chat.completions.create')
    def test_vision_with_detail_level(self, mock_create):
        """Test vision endpoint with detail parameter"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Detailed analysis"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/vision", json={
            "prompt": "Analyze in detail",
            "image_url": "https://example.com/image.jpg",
            "detail": "high"
        })
        
        assert response.status_code == 200
        
        # Verify that detail parameter was passed correctly
        call_args = mock_create.call_args
        messages = call_args.kwargs['messages']
        assert messages[0]['content'][1]['image_url']['detail'] == 'high'


class TestAudioTranscriptionEndpoint:
    """Test audio transcription endpoint
    
    TODO (Issue #32): Ensure response includes 'input_type' field
    TODO (Issue #32): Verify audio file upload handling works correctly
    """
    
    @patch('api.index.client.audio.transcriptions.create')
    def test_transcribe_audio(self, mock_create):
        """Test audio transcription with file upload"""
        mock_response = MagicMock()
        mock_response.text = "This is a test transcription."
        mock_create.return_value = mock_response
        
        # Create a fake audio file
        audio_content = b"fake audio data"
        files = {
            'file': ('test_audio.mp3', io.BytesIO(audio_content), 'audio/mpeg')
        }
        
        response = client.post("/ai/audio/transcribe", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "transcription" in data
        assert data["model"] == "whisper-1"
        # TODO (Issue #32): Fix endpoint to return input_type field
        assert data["input_type"] == "audio"
    
    @patch('api.index.client.audio.transcriptions.create')
    def test_transcribe_with_language(self, mock_create):
        """Test audio transcription with language parameter"""
        mock_response = MagicMock()
        mock_response.text = "Test transcription"
        mock_create.return_value = mock_response
        
        audio_content = b"fake audio data"
        files = {
            'file': ('test_audio.mp3', io.BytesIO(audio_content), 'audio/mpeg')
        }
        data = {
            'language': 'en'
        }
        
        response = client.post("/ai/audio/transcribe", files=files, data=data)
        
        assert response.status_code == 200
    
    @patch('api.index.client.audio.transcriptions.create')
    def test_transcribe_with_prompt(self, mock_create):
        """Test audio transcription with prompt for context"""
        mock_response = MagicMock()
        mock_response.text = "Test transcription with context"
        mock_create.return_value = mock_response
        
        audio_content = b"fake audio data"
        files = {
            'file': ('test_audio.mp3', io.BytesIO(audio_content), 'audio/mpeg')
        }
        data = {
            'prompt': 'This is a technical discussion about AI.'
        }
        
        response = client.post("/ai/audio/transcribe", files=files, data=data)
        
        assert response.status_code == 200


class TestImageGenerationEndpoint:
    """Test image generation endpoint"""
    
    @patch('api.index.client.images.generate')
    def test_generate_image_dalle3(self, mock_create):
        """Test image generation with DALL-E 3"""
        mock_response = MagicMock()
        mock_image = MagicMock()
        mock_image.url = "https://example.com/generated_image.png"
        mock_image.revised_prompt = "A detailed version of the prompt"
        mock_response.data = [mock_image]
        mock_create.return_value = mock_response
        
        response = client.post("/ai/image/generate", json={
            "prompt": "A beautiful sunset over mountains",
            "model": "dall-e-3"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "images" in data
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/generated_image.png"
        assert "revised_prompt" in data["images"][0]
    
    @patch('api.index.client.images.generate')
    def test_generate_image_dalle2(self, mock_create):
        """Test image generation with DALL-E 2"""
        mock_response = MagicMock()
        mock_image = MagicMock()
        mock_image.url = "https://example.com/generated_image.png"
        mock_response.data = [mock_image]
        mock_create.return_value = mock_response
        
        response = client.post("/ai/image/generate", json={
            "prompt": "A cat playing piano",
            "model": "dall-e-2",
            "size": "512x512"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["model"] == "dall-e-2"
    
    def test_generate_image_empty_prompt(self):
        """Test that image generation requires a prompt"""
        response = client.post("/ai/image/generate", json={
            "prompt": ""
        })
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_generate_image_invalid_size(self):
        """Test image generation with invalid size for model"""
        response = client.post("/ai/image/generate", json={
            "prompt": "A landscape",
            "model": "dall-e-3",
            "size": "256x256"  # Invalid for DALL-E 3
        })
        
        assert response.status_code == 400
        assert "Invalid size" in response.json()["detail"]
    
    @patch('api.index.client.images.generate')
    def test_generate_image_with_quality(self, mock_create):
        """Test image generation with quality parameter"""
        mock_response = MagicMock()
        mock_image = MagicMock()
        mock_image.url = "https://example.com/hd_image.png"
        mock_response.data = [mock_image]
        mock_create.return_value = mock_response
        
        response = client.post("/ai/image/generate", json={
            "prompt": "High quality artwork",
            "model": "dall-e-3",
            "quality": "hd"
        })
        
        assert response.status_code == 200
        
        # Verify quality parameter was passed
        call_args = mock_create.call_args
        assert call_args.kwargs['quality'] == 'hd'


class TestModelsEndpoint:
    """Test models listing and information endpoints
    
    TODO (Issue #32): Ensure /ai/models response includes 'total_count' field
    TODO (Issue #32): Ensure /ai/models response includes 'capabilities' breakdown
    TODO (Issue #32): Ensure /ai/models/{model_id} response includes 'model_name' field
    TODO (Issue #32): Verify model info endpoint returns proper structure
    """
    
    def test_list_models(self):
        """Test listing all supported models"""
        response = client.get("/ai/models")
        
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        # TODO (Issue #32): Fix endpoint to return total_count field
        assert "total_count" in data
        # TODO (Issue #32): Fix endpoint to return capabilities breakdown
        assert "capabilities" in data
        assert len(data["models"]) > 0
        
        # Check that different model types are present
        # TODO (Issue #32): Verify capabilities structure matches expected format
        assert "text" in data["capabilities"]
        assert "image_analysis" in data["capabilities"]
        assert "audio" in data["capabilities"]
    
    def test_get_model_info_valid(self):
        """Test getting information for a valid model"""
        response = client.get("/ai/models/gpt-3.5-turbo")
        
        assert response.status_code == 200
        data = response.json()
        # TODO (Issue #32): Fix endpoint to return model_name field
        assert data["model_name"] == "gpt-3.5-turbo"
        assert "capabilities" in data
        assert data["status"] == "available"
    
    def test_get_model_info_invalid(self):
        """Test getting information for an invalid model"""
        response = client.get("/ai/models/nonexistent-model")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestFineTuningEndpoint:
    """Test fine-tuning configuration endpoint
    
    TODO (Issue #32, #36): Fix validation to handle string vs int types for batch_size and learning_rate
    TODO (Issue #32, #36): Ensure hyperparameters are properly converted to correct types
    TODO (Issue #36): Add support for advanced fine-tuning features
    """
    
    def test_configure_fine_tuning(self):
        """Test configuring fine-tuning parameters"""
        response = client.post("/ai/fine-tune/configure", json={
            "training_file": "file-abc123",
            "model": "gpt-3.5-turbo",
            "n_epochs": 5
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "configuration" in data
        assert data["configuration"]["training_file"] == "file-abc123"
        assert data["configuration"]["model"] == "gpt-3.5-turbo"
        assert data["configuration"]["hyperparameters"]["n_epochs"] == 5
        assert data["status"] == "configured"
    
    def test_configure_fine_tuning_with_validation(self):
        """Test fine-tuning configuration with validation file"""
        response = client.post("/ai/fine-tune/configure", json={
            "training_file": "file-abc123",
            "validation_file": "file-xyz789",
            "model": "gpt-3.5-turbo",
            "suffix": "custom-model"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["configuration"]["validation_file"] == "file-xyz789"
        assert data["configuration"]["suffix"] == "custom-model"
    
    def test_configure_fine_tuning_with_hyperparameters(self):
        """Test fine-tuning configuration with custom hyperparameters"""
        response = client.post("/ai/fine-tune/configure", json={
            "training_file": "file-abc123",
            "n_epochs": 10,
            "batch_size": "4",
            "learning_rate_multiplier": "0.1"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["configuration"]["hyperparameters"]["n_epochs"] == 10
        assert data["configuration"]["hyperparameters"]["batch_size"] == "4"
        assert data["configuration"]["hyperparameters"]["learning_rate_multiplier"] == "0.1"


class TestMultiModalIntegration:
    """Test that multi-modal capabilities work together
    
    TODO (Issue #32): Ensure models endpoint returns capabilities breakdown
    TODO (Issue #32): Ensure model objects include model_name field
    TODO (Issue #32): Verify integration between different multimodal features
    """
    
    def test_models_endpoint_shows_all_capabilities(self):
        """Test that models endpoint shows text, image, and audio capabilities"""
        response = client.get("/ai/models")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all capability types are present
        # TODO (Issue #32): Fix endpoint to return capabilities field
        capabilities = data["capabilities"]
        assert len(capabilities["text"]) > 0
        assert len(capabilities["image_analysis"]) > 0
        assert len(capabilities["image_generation"]) > 0
        assert len(capabilities["audio"]) > 0
    
    def test_vision_model_in_model_list(self):
        """Test that vision models appear in the model list"""
        response = client.get("/ai/models")
        
        assert response.status_code == 200
        data = response.json()
        
        # Find vision model in the list
        # TODO (Issue #32): Fix model schema to include model_name field
        vision_models = [m for m in data["models"] if "vision" in m["model_name"].lower()]
        assert len(vision_models) > 0
        
        # Check it has both text and image capabilities
        vision_model = vision_models[0]
        assert "text" in vision_model["capabilities"]
        assert "image" in vision_model["capabilities"]
