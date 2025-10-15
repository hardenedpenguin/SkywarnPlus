"""
County ID audio file generator for SkywarnPlus.
"""

import os
import re
import logging
import requests
import zipfile
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import shutil

from .exceptions import AudioProcessingError, NetworkError, ValidationError
from .config import ConfigManager
from .data_types import CountyConfig


class CountyIDGenerator:
    """Generates WAV audio files for county names using TTS API."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize county ID generator."""
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
        
        # Audio processing
        self._AudioSegment = None
        self._split_on_silence = None
    
    def _lazy_import_pydub(self):
        """Lazy import pydub components."""
        if self._AudioSegment is None:
            try:
                from pydub import AudioSegment
                from pydub.silence import split_on_silence
                self._AudioSegment = AudioSegment
                self._split_on_silence = split_on_silence
            except ImportError:
                raise AudioProcessingError("pydub is required for audio processing")
        return self._AudioSegment, self._split_on_silence
    
    def sanitize_text_for_tts(self, text: str) -> str:
        """
        Sanitize text for TTS processing.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove special characters and normalize
        text = re.sub(r'[^\w\s\-\.]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def generate_wav(self, text: str, output_file: str) -> bool:
        """
        Generate WAV file from text using VoiceRSS API.
        
        Args:
            text: Text to convert to speech
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Sanitize text
            sanitized_text = self.sanitize_text_for_tts(text)
            
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
                "src": sanitized_text
            }
            
            if self.speed != "0":
                params["r"] = self.speed
            
            # Make API request
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Check if response is audio data
            content_type = response.headers.get("content-type", "")
            if "audio" not in content_type and "wav" not in content_type:
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
            
            self.logger.info(f"Generated WAV file: {output_file}")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"TTS API request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"WAV generation error: {e}")
            return False
    
    def optimize_audio(self, input_file: str, output_file: str) -> bool:
        """
        Optimize audio file by trimming silence and normalizing.
        
        Args:
            input_file: Input audio file path
            output_file: Output audio file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            AudioSegment, split_on_silence = self._lazy_import_pydub()
            
            # Load audio
            audio = AudioSegment.from_wav(input_file)
            
            # Split on silence to find speech segments
            chunks = split_on_silence(
                audio,
                min_silence_len=100,  # Minimum silence length in ms
                silence_thresh=audio.dBFS - 16,  # Silence threshold
                keep_silence=50  # Keep some silence at edges
            )
            
            if not chunks:
                self.logger.warning(f"No speech segments found in {input_file}")
                return False
            
            # Combine chunks
            optimized = sum(chunks)
            
            # Normalize audio
            normalized = optimized.normalize()
            
            # Export optimized audio
            normalized.export(output_file, format="wav")
            
            self.logger.info(f"Optimized audio saved: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Audio optimization failed: {e}")
            return False
    
    def backup_existing_files(self, path: str, filename_pattern: str, backup_name: str) -> None:
        """
        Backup existing files matching pattern.
        
        Args:
            path: Directory path to search
            filename_pattern: Pattern to match filenames
            backup_name: Name for backup directory
        """
        try:
            backup_dir = os.path.join(path, backup_name)
            os.makedirs(backup_dir, exist_ok=True)
            
            pattern = re.compile(filename_pattern)
            
            for filename in os.listdir(path):
                if pattern.match(filename):
                    src_file = os.path.join(path, filename)
                    dst_file = os.path.join(backup_dir, filename)
                    
                    if os.path.isfile(src_file):
                        shutil.copy2(src_file, dst_file)
                        self.logger.info(f"Backed up: {filename}")
            
            self.logger.info(f"Backup completed in: {backup_dir}")
            
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
    
    def load_county_codes_from_md(self, md_file_path: str) -> Dict[str, str]:
        """
        Load county codes and names from markdown file.
        
        Args:
            md_file_path: Path to CountyCodes.md file
            
        Returns:
            Dictionary mapping county codes to names
        """
        county_data = {}
        
        try:
            with open(md_file_path, "r") as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or not line.startswith("|"):
                    continue
                
                parts = line.split("|")
                if len(parts) >= 3:
                    code = parts[1].strip()
                    name = parts[2].strip()
                    
                    if code and name and code != "Code" and name != "Name":
                        county_data[code] = name
            
            self.logger.info(f"Loaded {len(county_data)} county codes from {md_file_path}")
            return county_data
            
        except Exception as e:
            self.logger.error(f"Failed to load county codes: {e}")
            return {}
    
    def process_county_codes(self, county_configs: List[CountyConfig], 
                           sounds_path: str, county_data: Dict[str, str]) -> bool:
        """
        Process county codes and generate audio files.
        
        Args:
            county_configs: List of county configurations
            sounds_path: Path to sounds directory
            county_data: County code to name mapping
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Backup existing files
            self.backup_existing_files(sounds_path, r".*\.wav$", "backup_" + 
                                     str(int(os.path.getctime(sounds_path))))
            
            success_count = 0
            total_count = len(county_configs)
            
            for config in county_configs:
                county_code = config.code
                county_name = county_data.get(county_code, county_code)
                
                # Generate filename
                filename = f"{county_name.replace(' ', '_')}.wav"
                output_file = os.path.join(sounds_path, filename)
                
                # Generate WAV file
                if self.generate_wav(county_name, output_file):
                    # Optimize audio
                    temp_file = output_file + ".temp"
                    if self.optimize_audio(output_file, temp_file):
                        os.replace(temp_file, output_file)
                        success_count += 1
                        self.logger.info(f"Successfully processed: {county_name}")
                    else:
                        self.logger.error(f"Failed to optimize: {county_name}")
                else:
                    self.logger.error(f"Failed to generate: {county_name}")
            
            self.logger.info(f"Processed {success_count}/{total_count} county audio files")
            return success_count == total_count
            
        except Exception as e:
            self.logger.error(f"County processing failed: {e}")
            return False
    
    def validate_config(self) -> bool:
        """Validate configuration."""
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
            self.logger.error(f"Configuration validation failed: {e}")
            return False
