"""
Text-to-Speech processing functionality for SkywarnPlus.
"""

import os
import re
import logging
import requests
import urllib.parse
from typing import Dict, Any, Optional

from .exceptions import AudioProcessingError, NetworkError, ValidationError
from .config import ConfigManager


class TTSProcessor:
    """Handles text-to-speech conversion using VoiceRSS API."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize TTS processor."""
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Get TTS configuration
        tts_config = self.config_manager.get_tts_config()
        if not tts_config:
            raise ValidationError("TTS configuration not found")
        
        self.api_key = tts_config.get("api_key")
        self.language = tts_config.get("language", "en-us")
        self.voice = tts_config.get("voice", "John")
        self.speed = tts_config.get("speed", "0")
        self.format = tts_config.get("format", "8khz_16bit_mono")
        
        if not self.api_key:
            raise ValidationError("VoiceRSS API key not found in configuration")
    
    def modify_description(self, description: str) -> str:
        """
        Modify the description to make it more suitable for TTS conversion.
        
        Args:
            description: The description text to modify
            
        Returns:
            Modified description text
        """
        # Remove newline characters and replace multiple spaces with a single space
        description = description.replace("\n", " ")
        description = re.sub(r"\s+", " ", description)
        
        # Replace common weather abbreviations and symbols
        abbreviations = {
            r"\bmph\b": "miles per hour",
            r"\bknots\b": "nautical miles per hour",
            r"\bNm\b": "nautical miles",
            r"\bnm\b": "nautical miles",
            r"\bft\.\b": "feet",
            r"\bin\.\b": "inches",
            r"\bm\b": "meter",
            r"\bkm\b": "kilometer",
            r"\bmi\b": "mile",
            r"\b%\b": "percent",
            r"\bN\b": "north",
            r"\bS\b": "south",
            r"\bE\b": "east",
            r"\bW\b": "west",
            r"\bNE\b": "northeast",
            r"\bNW\b": "northwest",
            r"\bSE\b": "southeast",
            r"\bSW\b": "southwest",
            r"\bF\b": "Fahrenheit",
            r"\bC\b": "Celsius",
            r"\bUV\b": "ultraviolet",
            r"\bgusts up to\b": "gusts of up to",
            r"\bhrs\b": "hours",
            r"\bhr\b": "hour",
            r"\bmin\b": "minute",
            r"\bsec\b": "second",
            r"\bsq\b": "square",
            r"\bw/\b": "with",
            r"\bc/o\b": "care of",
            r"\bblw\b": "below",
            r"\babv\b": "above",
            r"\bavg\b": "average",
            r"\bfr\b": "from",
            r"\bto\b": "to",
            r"\btill\b": "until",
            r"\bb/w\b": "between",
            r"\bbtwn\b": "between",
            r"\bN/A\b": "not available",
            r"\b&\b": "and",
            r"\b\+\b": "plus",
            r"\be\.g\.\b": "for example",
            r"\bi\.e\.\b": "that is",
            r"\best\.\b": "estimated",
            r"\b\.\.\.\b": ".",
            r"\b\n\n\b": ".",
            r"\b\n\b": ".",
            r"\bEDT\b": "eastern daylight time",
            r"\bEST\b": "eastern standard time",
            r"\bCST\b": "central standard time",
            r"\bCDT\b": "central daylight time",
            r"\bMST\b": "mountain standard time",
            r"\bMDT\b": "mountain daylight time",
            r"\bPST\b": "pacific standard time",
            r"\bPDT\b": "pacific daylight time",
            r"\bAKST\b": "alaska standard time",
            r"\bAKDT\b": "alaska daylight time",
            r"\bHST\b": "hawaii standard time",
            r"\bHADT\b": "hawaii daylight time",
            r"\bUTC\b": "coordinated universal time",
            r"\bGMT\b": "greenwich mean time",
        }
        
        # Apply abbreviations
        for pattern, replacement in abbreviations.items():
            description = re.sub(pattern, replacement, description, flags=re.IGNORECASE)
        
        # Clean up multiple periods and spaces
        description = re.sub(r"\.+", ".", description)
        description = re.sub(r"\s+", " ", description)
        description = description.strip()
        
        return description
    
    def convert_to_audio(self, text: str, output_file: str) -> bool:
        """
        Convert text to audio using VoiceRSS API.
        
        Args:
            text: Text to convert to speech
            output_file: Output file path for the audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Modify text for better TTS
            modified_text = self.modify_description(text)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Build API URL
            api_url = "http://api.voicerss.org/"
            params = {
                "key": self.api_key,
                "hl": self.language,
                "f": self.format,
                "v": self.voice,
                "c": "WAV",
                "src": modified_text
            }
            
            if self.speed != "0":
                params["r"] = self.speed
            
            # Make API request
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Check if response is audio data
            content_type = response.headers.get("content-type", "")
            if "audio" not in content_type and "wav" not in content_type:
                # Try to parse error message
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", "Unknown error")
                    self.logger.error(f"VoiceRSS API error: {error_msg}")
                    return False
                except:
                    self.logger.error(f"VoiceRSS API returned non-audio content: {content_type}")
                    return False
            
            # Save audio file
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            self.logger.info(f"TTS audio saved to: {output_file}")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"TTS API request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"TTS conversion error: {e}")
            return False
    
    def get_available_voices(self) -> list:
        """Get list of available voices from VoiceRSS."""
        # This would require additional API call or documentation
        # For now, return common voices
        return ["John", "Mary", "Mike", "Linda", "James", "Sarah"]
    
    def validate_config(self) -> bool:
        """Validate TTS configuration."""
        try:
            if not self.api_key:
                self.logger.error("VoiceRSS API key is missing")
                return False
            
            if not self.language:
                self.logger.error("TTS language is not configured")
                return False
            
            if not self.voice:
                self.logger.error("TTS voice is not configured")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"TTS configuration validation failed: {e}")
            return False
