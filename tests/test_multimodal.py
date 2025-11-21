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
    """Test vision/image analysis endpoint"""
    
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
    """Test audio transcription endpoint"""
    
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
    """Test models listing and information endpoints"""
    
    def test_list_models(self):
        """Test listing all supported models"""
        response = client.get("/ai/models")
        
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "total_count" in data
        assert "capabilities" in data
        assert len(data["models"]) > 0
        
        # Check that different model types are present
        assert "text" in data["capabilities"]
        assert "image_analysis" in data["capabilities"]
        assert "audio" in data["capabilities"]
    
    def test_get_model_info_valid(self):
        """Test getting information for a valid model"""
        response = client.get("/ai/models/gpt-3.5-turbo")
        
        assert response.status_code == 200
        data = response.json()
        assert data["model_name"] == "gpt-3.5-turbo"
        assert "capabilities" in data
        assert data["status"] == "available"
    
    def test_get_model_info_invalid(self):
        """Test getting information for an invalid model"""
        response = client.get("/ai/models/nonexistent-model")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestFineTuningEndpoint:
    """Test fine-tuning configuration endpoint"""
    
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
    """Test that multi-modal capabilities work together"""
    
    def test_models_endpoint_shows_all_capabilities(self):
        """Test that models endpoint shows text, image, and audio capabilities"""
        response = client.get("/ai/models")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all capability types are present
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
        vision_models = [m for m in data["models"] if "vision" in m["model_name"].lower()]
        assert len(vision_models) > 0
        
        # Check it has both text and image capabilities
        vision_model = vision_models[0]
        assert "text" in vision_model["capabilities"]
        assert "image" in vision_model["capabilities"]


# ============================================================================
# TODO: ADDITIONAL TEST STUBS - Reference Issue #32 and Issue #36
# ============================================================================
# The following test stubs outline additional test coverage needed for
# comprehensive multimodal feature validation. Implement these tests
# before finalizing the multimodal PR.
# ============================================================================


# ----------------------------------------------------------------------------
# Vision Endpoint - Additional Tests Needed
# ----------------------------------------------------------------------------
class TestVisionEndpointAdditional:
    """TODO: Additional vision endpoint tests - Issue #32"""
    
    def test_vision_invalid_url(self):
        """TODO: Test vision endpoint with invalid/malformed image URL"""
        # Test cases:
        # - Non-existent URL
        # - Invalid URL format
        # - URL pointing to non-image content
        # Expected: 400 Bad Request with descriptive error
        pass
    
    def test_vision_malformed_base64(self):
        """TODO: Test vision endpoint with malformed base64 data"""
        # Test cases:
        # - Invalid base64 encoding
        # - Base64 that doesn't decode to image
        # - Empty base64 string
        # Expected: 400 Bad Request
        pass
    
    def test_vision_large_image_handling(self):
        """TODO: Test vision endpoint with very large images"""
        # Test cases:
        # - Image exceeding size limits
        # - High resolution images
        # Expected: Appropriate error or successful handling
        pass
    
    def test_vision_max_tokens_validation(self):
        """TODO: Test vision endpoint max_tokens parameter validation"""
        # Test cases:
        # - max_tokens exceeding model limit (2048)
        # - Negative max_tokens
        # - Zero max_tokens
        # Expected: 400 for invalid values
        pass
    
    def test_vision_openai_error_handling(self):
        """TODO: Test vision endpoint handles OpenAI API failures gracefully"""
        # Test cases:
        # - API rate limit errors
        # - API server errors
        # - Network timeouts
        # Expected: Appropriate error responses with retry guidance
        pass
    
    def test_vision_with_session_id(self):
        """TODO: Test vision endpoint with session_id for conversation history"""
        # Test cases:
        # - Vision query with session_id creates history
        # - Follow-up text questions reference vision context
        # - History retrieval includes vision interactions
        # Expected: Vision queries integrated into conversation flow
        pass


# ----------------------------------------------------------------------------
# Audio Transcription - Additional Tests Needed
# ----------------------------------------------------------------------------
class TestAudioTranscriptionAdditional:
    """TODO: Additional audio transcription tests - Issue #32"""
    
    def test_audio_unsupported_format(self):
        """TODO: Test audio transcription with unsupported file formats"""
        # Test cases:
        # - .txt file instead of audio
        # - Unsupported audio codec
        # - Video file
        # Expected: 400 Bad Request with supported formats list
        pass
    
    def test_audio_file_size_limits(self):
        """TODO: Test audio transcription with file size limits"""
        # Test cases:
        # - File exceeding 25MB limit
        # - Empty file
        # - Very small file
        # Expected: Appropriate validation errors
        pass
    
    def test_audio_timestamp_options(self):
        """TODO: Test audio transcription with timestamp options"""
        # Test cases:
        # - Request with timestamp_granularities
        # - Verify timestamps in response
        # Expected: Response includes word/segment timestamps
        pass
    
    def test_audio_response_formats(self):
        """TODO: Test audio transcription different response formats"""
        # Test cases:
        # - response_format: json
        # - response_format: text
        # - response_format: srt
        # - response_format: vtt
        # Expected: Correct format returned for each type
        pass
    
    def test_audio_temperature_parameter(self):
        """TODO: Test audio transcription temperature parameter"""
        # Test cases:
        # - Temperature between 0 and 1
        # - Temperature outside valid range
        # Expected: Valid values accepted, invalid rejected
        pass
    
    def test_audio_corrupted_file(self):
        """TODO: Test audio transcription with corrupted audio files"""
        # Test cases:
        # - Truncated audio file
        # - Corrupted header
        # Expected: Graceful error handling
        pass
    
    def test_audio_translation_endpoint(self):
        """TODO: Test audio translation endpoint if implemented"""
        # Test cases:
        # - Translation of non-English audio to English
        # - Verify POST /ai/audio/translate endpoint
        # Expected: Translated text in response
        pass
    
    def test_audio_no_file_upload(self):
        """TODO: Test audio endpoint without file upload"""
        # Test case: POST to /ai/audio/transcribe without file
        # Expected: 400 Bad Request - file required
        pass


# ----------------------------------------------------------------------------
# Image Generation - Additional Tests Needed
# ----------------------------------------------------------------------------
class TestImageGenerationAdditional:
    """TODO: Additional image generation tests - Issue #32"""
    
    def test_image_gen_multiple_images(self):
        """TODO: Test image generation with n parameter (multiple images)"""
        # Test cases:
        # - n=2, n=3, n=4 for DALL-E 2
        # - n>1 for DALL-E 3 (should fail - only supports n=1)
        # - n=0 or negative
        # Expected: Correct number of images returned or validation error
        pass
    
    def test_image_gen_all_sizes(self):
        """TODO: Test image generation with different size options"""
        # DALL-E 3 sizes: 1024x1024, 1792x1024, 1024x1792
        # DALL-E 2 sizes: 256x256, 512x512, 1024x1024
        # Expected: Correct size validation per model
        pass
    
    def test_image_gen_style_parameter(self):
        """TODO: Test image generation with style parameter (DALL-E 3)"""
        # Test cases:
        # - style: "vivid"
        # - style: "natural"
        # - Invalid style value
        # Expected: Style applied correctly for DALL-E 3
        pass
    
    def test_image_gen_prompt_length_limits(self):
        """TODO: Test image generation prompt length validation"""
        # Test cases:
        # - Very long prompts (>4000 characters)
        # - Empty or whitespace-only prompts
        # Expected: Appropriate validation errors
        pass
    
    def test_image_gen_content_policy_violation(self):
        """TODO: Test image generation content policy error handling"""
        # Test case: Mock OpenAI content policy violation
        # Expected: Graceful error message to user
        pass
    
    def test_image_gen_revised_prompt(self):
        """TODO: Test image generation revised_prompt handling"""
        # Test case: Verify revised_prompt returned by DALL-E 3
        # Expected: Original and revised prompts in response
        pass
    
    def test_image_edit_endpoint(self):
        """TODO: Test image edit endpoint if implemented"""
        # Test cases:
        # - POST /ai/image/edit with image and mask
        # - Verify edited image returned
        # Expected: Endpoint available and functional
        pass
    
    def test_image_variation_endpoint(self):
        """TODO: Test image variation endpoint if implemented"""
        # Test cases:
        # - POST /ai/image/variation with source image
        # - Verify variations returned
        # Expected: Endpoint available and functional
        pass


# ----------------------------------------------------------------------------
# Model Listing - Additional Tests Needed
# ----------------------------------------------------------------------------
class TestModelsEndpointAdditional:
    """TODO: Additional model listing tests - Issue #32"""
    
    def test_list_models_filter_by_type(self):
        """TODO: Test filtering models by type"""
        # Test cases:
        # - Filter by type=text
        # - Filter by type=vision
        # - Filter by type=audio
        # - Filter by type=multimodal
        # Expected: Only models of specified type returned
        pass
    
    def test_list_models_filter_by_capability(self):
        """TODO: Test filtering models by capability"""
        # Test cases:
        # - Filter by supports_streaming=true
        # - Filter by supports_fine_tuning=true
        # Expected: Only models with capability returned
        pass
    
    def test_model_info_metadata(self):
        """TODO: Test model information includes all required metadata"""
        # Verify response includes:
        # - model_id, name, type, description
        # - max_tokens, supports_streaming, supports_fine_tuning
        # Expected: Complete metadata for each model
        pass
    
    def test_model_availability_status(self):
        """TODO: Test model availability status"""
        # Test cases:
        # - Check status field (available/deprecated/beta)
        # - Verify deprecated models marked appropriately
        # Expected: Accurate status information
        pass


# ----------------------------------------------------------------------------
# Fine-Tuning - Additional Tests Needed
# ----------------------------------------------------------------------------
class TestFineTuningAdditional:
    """TODO: Additional fine-tuning tests - Issue #36"""
    
    def test_fine_tune_invalid_training_file(self):
        """TODO: Test fine-tuning with invalid training_file ID"""
        # Test cases:
        # - Non-existent file ID
        # - Malformed file ID
        # Expected: 400 Bad Request
        pass
    
    def test_fine_tune_n_epochs_bounds(self):
        """TODO: Test fine-tuning n_epochs validation (1-50)"""
        # Test cases:
        # - n_epochs = 0
        # - n_epochs = 51
        # - n_epochs = -1
        # Expected: 400 for out-of-range values
        pass
    
    def test_fine_tune_batch_size_bounds(self):
        """TODO: Test fine-tuning batch_size validation (1-256)"""
        # Test cases:
        # - batch_size = 0
        # - batch_size = 257
        # - batch_size = "auto"
        # Expected: Validation per OpenAI requirements
        pass
    
    def test_fine_tune_learning_rate_bounds(self):
        """TODO: Test fine-tuning learning_rate_multiplier validation"""
        # Test cases:
        # - learning_rate_multiplier = 0
        # - learning_rate_multiplier > 10
        # - Negative values
        # Expected: 400 for invalid values
        pass
    
    def test_fine_tune_unsupported_model(self):
        """TODO: Test fine-tuning with unsupported model"""
        # Test cases:
        # - Try to fine-tune GPT-4 (not supported)
        # - Try to fine-tune vision models
        # Expected: 400 with supported models list
        pass
    
    def test_fine_tune_job_creation(self):
        """TODO: Test fine-tuning job creation if implemented"""
        # Test cases:
        # - POST /ai/fine-tune/jobs to create job
        # - Verify job ID returned
        # Expected: Job created successfully
        pass
    
    def test_fine_tune_job_status(self):
        """TODO: Test fine-tuning job status checking if implemented"""
        # Test cases:
        # - GET /ai/fine-tune/jobs/{job_id}
        # - Verify status updates (queued/running/succeeded/failed)
        # Expected: Accurate job status
        pass
    
    def test_fine_tune_job_cancellation(self):
        """TODO: Test fine-tuning job cancellation if implemented"""
        # Test cases:
        # - POST /ai/fine-tune/jobs/{job_id}/cancel
        # - Verify job cancelled
        # Expected: Job cancellation successful
        pass
    
    def test_fine_tune_list_jobs(self):
        """TODO: Test listing fine-tuning jobs if implemented"""
        # Test cases:
        # - GET /ai/fine-tune/jobs
        # - Verify pagination
        # Expected: List of jobs returned
        pass


# ----------------------------------------------------------------------------
# Integration Tests - Additional Coverage Needed
# ----------------------------------------------------------------------------
class TestMultiModalIntegrationAdditional:
    """TODO: Additional integration tests - Issue #32"""
    
    def test_switch_model_types_same_session(self):
        """TODO: Test switching between model types in same session"""
        # Test cases:
        # - Text chat -> Vision -> Text in same session
        # - Verify context maintained appropriately
        # Expected: Smooth transitions between modalities
        pass
    
    def test_vision_in_conversation(self):
        """TODO: Test combining text chat with vision in conversation"""
        # Test cases:
        # - Ask about image, then follow-up text questions
        # - Verify AI references vision context
        # Expected: Coherent multi-turn vision conversations
        pass
    
    def test_resource_limits_multimodal(self):
        """TODO: Test resource limits across modalities"""
        # Test cases:
        # - Concurrent vision + audio + text requests
        # - Session history limits with mixed content
        # Expected: Fair resource allocation
        pass
    
    def test_error_handling_consistency(self):
        """TODO: Test error handling consistency across endpoints"""
        # Test cases:
        # - Similar errors from different endpoints
        # - Verify error format consistency
        # Expected: Uniform error response structure
        pass
    
    def test_rate_limiting_multimodal(self):
        """TODO: Test rate limiting across multimodal endpoints"""
        # Test cases:
        # - Rapid requests to different endpoints
        # - Verify rate limits apply correctly
        # Expected: Rate limiting enforced consistently
        pass


# ----------------------------------------------------------------------------
# Performance Tests - Benchmarks Needed
# ----------------------------------------------------------------------------
class TestMultiModalPerformance:
    """TODO: Performance benchmarks - Issue #32"""
    
    def test_vision_response_time(self):
        """TODO: Benchmark vision endpoint response time"""
        # Measure and assert reasonable response times
        # Target: < 10 seconds for typical vision query
        pass
    
    def test_audio_transcription_response_time(self):
        """TODO: Benchmark audio transcription response time"""
        # Measure transcription time for various audio lengths
        # Target: Proportional to audio duration
        pass
    
    def test_image_generation_response_time(self):
        """TODO: Benchmark image generation response time"""
        # Measure generation time for different models
        # Target: < 30 seconds for DALL-E 3
        pass
    
    def test_concurrent_requests(self):
        """TODO: Test concurrent request handling"""
        # Test cases:
        # - Multiple simultaneous vision requests
        # - Mixed endpoint concurrent requests
        # Expected: No significant degradation
        pass
    
    def test_memory_usage_large_files(self):
        """TODO: Test memory usage with large files"""
        # Monitor memory during:
        # - Large image processing
        # - Long audio file transcription
        # Expected: Memory usage within limits
        pass
    
    def test_timeout_handling(self):
        """TODO: Test timeout handling for long operations"""
        # Test cases:
        # - Very long audio transcription
        # - Complex image generation
        # Expected: Graceful timeout handling
        pass


# ============================================================================
# EXAMPLE REQUEST/RESPONSE FIXTURES
# ============================================================================
# TODO: Use these fixtures in tests for consistency - Issue #32
# ============================================================================

# Vision request/response examples
VISION_REQUEST_EXAMPLE = {
    "prompt": "What objects are in this image?",
    "image_url": "https://example.com/test-image.jpg",
    "max_tokens": 300,
    "detail": "high"
}

VISION_RESPONSE_EXAMPLE = {
    "response": "I can see a cat sitting on a windowsill, looking outside...",
    "model": "gpt-4-vision-preview",
    "input_type": "image",
    "image_url": "https://example.com/test-image.jpg"
}

# Audio transcription request/response examples
AUDIO_REQUEST_EXAMPLE = {
    "file": "audio_file.mp3",  # Multipart file upload
    "language": "en",
    "prompt": "This is a technical discussion about AI."
}

AUDIO_RESPONSE_EXAMPLE = {
    "transcription": "Hello, this is a test transcription of the audio file.",
    "model": "whisper-1",
    "input_type": "audio",
    "language": "en"
}

# Image generation request/response examples
IMAGE_GEN_REQUEST_EXAMPLE = {
    "prompt": "A serene mountain landscape at sunset with vibrant colors",
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "hd",
    "n": 1,
    "style": "vivid"
}

IMAGE_GEN_RESPONSE_EXAMPLE = {
    "images": [
        {
            "url": "https://example.com/generated-image.png",
            "revised_prompt": "A serene mountain landscape at golden hour sunset..."
        }
    ],
    "prompt": "A serene mountain landscape at sunset with vibrant colors",
    "model": "dall-e-3"
}

# Model list response example
MODEL_LIST_RESPONSE_EXAMPLE = {
    "models": [
        {
            "model_name": "gpt-3.5-turbo",
            "type": "text",
            "capabilities": ["text", "chat"],
            "status": "available",
            "supports_streaming": True,
            "supports_fine_tuning": True
        },
        {
            "model_name": "gpt-4-vision-preview",
            "type": "vision",
            "capabilities": ["text", "image"],
            "status": "available",
            "supports_streaming": False,
            "supports_fine_tuning": False
        }
    ],
    "total_count": 8,
    "capabilities": {
        "text": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        "image_analysis": ["gpt-4-vision-preview", "gpt-4o"],
        "image_generation": ["dall-e-2", "dall-e-3"],
        "audio": ["whisper-1"]
    }
}

# Fine-tuning configuration request/response examples
FINE_TUNE_REQUEST_EXAMPLE = {
    "training_file": "file-abc123xyz",
    "validation_file": "file-def456uvw",
    "model": "gpt-3.5-turbo",
    "n_epochs": 3,
    "batch_size": "auto",
    "learning_rate_multiplier": "auto",
    "suffix": "my-custom-model"
}

FINE_TUNE_RESPONSE_EXAMPLE = {
    "configuration": {
        "training_file": "file-abc123xyz",
        "validation_file": "file-def456uvw",
        "model": "gpt-3.5-turbo",
        "suffix": "my-custom-model",
        "hyperparameters": {
            "n_epochs": 3,
            "batch_size": "auto",
            "learning_rate_multiplier": "auto"
        }
    },
    "status": "configured",
    "message": "Fine-tuning configuration saved successfully"
}

# Error response example (consistent format)
ERROR_RESPONSE_EXAMPLE = {
    "detail": "Validation error: max_tokens must be between 1 and 2048",
    "error_code": "VALIDATION_ERROR",
    "status_code": 400
}
