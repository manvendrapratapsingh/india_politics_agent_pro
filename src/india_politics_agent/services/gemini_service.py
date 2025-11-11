"""Gemini API service with multi-model fallback."""

import google.generativeai as genai
from typing import Optional, List
from ..utils.logging import get_logger
from ..utils.errors import APIError, QuotaExhaustedError

logger = get_logger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""

    def __init__(self, api_key: str, models: Optional[List[str]] = None):
        """
        Initialize Gemini service.

        Args:
            api_key: Gemini API key
            models: List of model names to try (in order)
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)

        self.models = models or [
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro-latest'
        ]

        logger.info(
            "GeminiService initialized",
            models=self.models
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 8000
    ) -> str:
        """
        Generate content using Gemini with multi-model fallback.

        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_output_tokens: Maximum tokens to generate

        Returns:
            Generated text

        Raises:
            APIError: If all models fail
        """
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        last_error = None

        for model_name in self.models:
            try:
                logger.info(f"Trying model: {model_name}")

                model = genai.GenerativeModel(model_name)

                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                    ),
                    safety_settings=safety_settings
                )

                if response.text:
                    logger.info(
                        "Generation successful",
                        model=model_name,
                        output_length=len(response.text)
                    )
                    return response.text
                else:
                    logger.warning(f"Empty response from {model_name}")

            except Exception as e:
                error_msg = str(e).lower()
                last_error = e

                if 'resource_exhausted' in error_msg or 'quota' in error_msg:
                    logger.warning(f"{model_name}: Quota exhausted")
                elif '404' in error_msg or 'not found' in error_msg:
                    logger.warning(f"{model_name}: Model not found")
                else:
                    logger.warning(f"{model_name} failed: {e}")

                # Try next model
                continue

        # All models failed
        raise APIError(
            f"All Gemini models failed. Last error: {last_error}",
            api_name="gemini"
        )
