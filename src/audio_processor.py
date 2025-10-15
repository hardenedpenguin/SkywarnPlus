"""
Audio processing functionality for SkywarnPlus.
"""

import os
import logging
import threading
from typing import Dict, Optional, List
from pathlib import Path
import gc

from .exceptions import AudioProcessingError
from .data_types import AudioConfig


class AudioProcessor:
    """Handles audio processing operations."""
    
    def __init__(self, config: AudioConfig):
        """Initialize audio processor."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._audio_cache: Dict[str, any] = {}
        self._cache_lock = threading.RLock()
        self._AudioSegment = None
    
    def _lazy_import_pydub(self):
        """Lazy import pydub to avoid loading unless needed."""
        if self._AudioSegment is None:
            try:
                from pydub import AudioSegment
                self._AudioSegment = AudioSegment
            except ImportError:
                raise AudioProcessingError("pydub is required for audio processing")
        return self._AudioSegment
    
    def _get_cached_audio(self, file_path: str) -> any:
        """Get audio file from cache or load it."""
        with self._cache_lock:
            if file_path not in self._audio_cache:
                try:
                    AudioSegment = self._lazy_import_pydub()
                    audio = AudioSegment.from_wav(file_path)
                    self._audio_cache[file_path] = audio
                    self.logger.debug(f"Loaded audio file: {file_path}")
                except Exception as e:
                    self.logger.error(f"Failed to load audio file {file_path}: {e}")
                    return None
            return self._audio_cache[file_path]
    
    def _create_silence_cached(self, duration_ms: int) -> any:
        """Create silence audio segment with caching."""
        cache_key = f"silence_{duration_ms}"
        with self._cache_lock:
            if cache_key not in self._audio_cache:
                try:
                    AudioSegment = self._lazy_import_pydub()
                    silence = AudioSegment.silent(duration=duration_ms)
                    self._audio_cache[cache_key] = silence
                except Exception as e:
                    self.logger.error(f"Failed to create silence: {e}")
                    return None
            return self._audio_cache[cache_key]
    
    def load_audio_file(self, file_path: str) -> Optional[any]:
        """Load an audio file."""
        if not os.path.exists(file_path):
            self.logger.error(f"Audio file not found: {file_path}")
            return None
        
        return self._get_cached_audio(file_path)
    
    def create_silence(self, duration_ms: int) -> Optional[any]:
        """Create a silence audio segment."""
        return self._create_silence_cached(duration_ms)
    
    def combine_audio(self, audio_segments: List[any]) -> Optional[any]:
        """Combine multiple audio segments."""
        if not audio_segments:
            return None
        
        try:
            AudioSegment = self._lazy_import_pydub()
            combined = AudioSegment.empty()
            
            for segment in audio_segments:
                if segment is not None:
                    combined += segment
            
            return combined
        except Exception as e:
            self.logger.error(f"Failed to combine audio segments: {e}")
            return None
    
    def export_audio(self, audio: any, output_path: str, format: str = "wav") -> bool:
        """Export audio to file."""
        try:
            if audio is None:
                self.logger.error("Cannot export None audio")
                return False
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Export audio
            audio.export(output_path, format=format)
            self.logger.debug(f"Exported audio to: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export audio to {output_path}: {e}")
            return False
    
    def batch_export_audio(self, exports: List[tuple]) -> bool:
        """Export multiple audio files in batch."""
        success_count = 0
        
        for audio, output_path, format in exports:
            if self.export_audio(audio, output_path, format):
                success_count += 1
        
        self.logger.info(f"Batch export completed: {success_count}/{len(exports)} successful")
        return success_count == len(exports)
    
    def cleanup_cache(self):
        """Clean up audio cache and free memory."""
        with self._cache_lock:
            self._audio_cache.clear()
            gc.collect()
            self.logger.debug("Audio cache cleaned up")
    
    def get_cache_size(self) -> int:
        """Get current cache size."""
        with self._cache_lock:
            return len(self._audio_cache)
