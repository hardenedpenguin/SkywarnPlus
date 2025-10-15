"""
State management for SkywarnPlus.
"""

import os
import json
import threading
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from .exceptions import FileIOError
from .data_types import StateData


class StateManager:
    """Manages application state persistence."""
    
    def __init__(self, data_file: str = "data.json"):
        """Initialize state manager."""
        self.data_file = data_file
        self.logger = logging.getLogger(__name__)
        self._state_cache: Dict[str, Any] = {}
        self._state_dirty = False
        self._state_lock = threading.RLock()
    
    def load_state(self) -> StateData:
        """Load state from file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as file:
                    state = json.load(file)
                    self.logger.debug(f"Loaded state from {self.data_file}")
            else:
                state = {
                    "last_alerts": {},
                    "last_sayalert": {},
                    "last_tailmessage": {},
                    "last_allclear": {},
                    "last_alert_script": {}
                }
                self.logger.info(f"Created new state file: {self.data_file}")
            
            # Update cache
            with self._state_lock:
                self._state_cache = state.copy()
                self._state_dirty = False
            
            return state
        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")
            raise FileIOError(f"Failed to load state: {e}")
    
    def save_state(self, state: StateData) -> None:
        """Save state to file with optimized I/O."""
        with self._state_lock:
            try:
                # Convert sets to lists for JSON serialization
                state_for_json = {}
                for key, value in state.items():
                    if isinstance(value, set):
                        state_for_json[key] = list(value)
                    elif isinstance(value, dict):
                        state_for_json[key] = {
                            k: list(v) if isinstance(v, set) else v
                            for k, v in value.items()
                        }
                    else:
                        state_for_json[key] = value
                
                # Update cache and mark as dirty
                self._state_cache = state_for_json.copy()
                self._state_dirty = True
                
                self.logger.debug("State updated in cache")
            except Exception as e:
                self.logger.error(f"Failed to update state cache: {e}")
                raise FileIOError(f"Failed to update state cache: {e}")
    
    def flush_state(self) -> None:
        """Flush cached state to disk atomically."""
        with self._state_lock:
            if not self._state_dirty:
                return
            
            # Atomic write using temporary file
            temp_file = self.data_file + '.tmp'
            try:
                with open(temp_file, "w") as file:
                    json.dump(self._state_cache, file, ensure_ascii=False, indent=4)
                os.replace(temp_file, self.data_file)
                self._state_dirty = False
                self.logger.debug(f"State flushed to {self.data_file}")
            except Exception as e:
                self.logger.error(f"Failed to save state: {e}")
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                raise FileIOError(f"Failed to save state: {e}")
    
    def get_state_value(self, key: str, default: Any = None) -> Any:
        """Get a value from the current state cache."""
        with self._state_lock:
            return self._state_cache.get(key, default)
    
    def set_state_value(self, key: str, value: Any) -> None:
        """Set a value in the current state cache."""
        with self._state_lock:
            self._state_cache[key] = value
            self._state_dirty = True
    
    def is_dirty(self) -> bool:
        """Check if state has unsaved changes."""
        with self._state_lock:
            return self._state_dirty
