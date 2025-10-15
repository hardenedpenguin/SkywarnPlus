"""
Alert announcement functionality for SkywarnPlus.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

from .audio_processor import AudioProcessor
from .asterisk_integration import AsteriskIntegration
from .alert_processor import AlertProcessor
from .exceptions import AudioProcessingError
from .data_types import AlertData, AudioConfig, AsteriskConfig, CountyConfig


class AlertAnnouncer:
    """Handles alert announcements and audio generation."""
    
    def __init__(self, audio_config: AudioConfig, asterisk_config: AsteriskConfig,
                 county_configs: List[CountyConfig]):
        """Initialize alert announcer."""
        self.audio_config = audio_config
        self.asterisk_config = asterisk_config
        self.county_configs = county_configs
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.audio_processor = AudioProcessor(audio_config)
        self.asterisk_integration = AsteriskIntegration(asterisk_config)
        self.alert_processor = AlertProcessor()
        
        # Create county lookup
        self.county_lookup = {config.code: config for config in county_configs}
    
    def say_alerts(self, alerts: Dict[str, List[AlertData]], 
                   max_alerts: int = 99) -> bool:
        """Generate and announce alert audio."""
        try:
            # Limit number of alerts
            limited_alerts = dict(list(alerts.items())[:max_alerts])
            
            # Generate audio for each alert
            audio_segments = []
            
            for alert_type, alert_list in limited_alerts.items():
                alert_audio = self._generate_alert_audio(alert_type, alert_list)
                if alert_audio:
                    audio_segments.append(alert_audio)
            
            if not audio_segments:
                self.logger.info("No alerts to announce")
                return True
            
            # Combine all alert audio
            combined_audio = self.audio_processor.combine_audio(audio_segments)
            if not combined_audio:
                self.logger.error("Failed to combine alert audio")
                return False
            
            # Add alert suffix if configured
            if self.audio_config.say_alert_suffix:
                suffix_path = os.path.join(self.audio_config.sounds_path, 
                                         self.audio_config.say_alert_suffix)
                suffix_audio = self.audio_processor.load_audio_file(suffix_path)
                if suffix_audio:
                    combined_audio += suffix_audio
            
            # Export audio file
            output_path = os.path.join("/tmp", "SkywarnPlus", "alert.wav")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.audio_processor.export_audio(combined_audio, output_path):
                return False
            
            # Convert to Asterisk format
            if not self.asterisk_integration.convert_audio(output_path):
                return False
            
            # Send to nodes
            ulaw_path = output_path.replace('.wav', '.ulaw')
            return self.asterisk_integration.send_to_nodes(ulaw_path)
            
        except Exception as e:
            self.logger.error(f"Error announcing alerts: {e}")
            return False
    
    def say_all_clear(self) -> bool:
        """Generate and announce all clear audio."""
        try:
            # Load all clear sound
            all_clear_path = os.path.join(
                self.audio_config.sounds_path, 
                "ALERTS", 
                self.audio_config.all_clear_sound
            )
            
            all_clear_audio = self.audio_processor.load_audio_file(all_clear_path)
            if not all_clear_audio:
                self.logger.error("Failed to load all clear audio")
                return False
            
            # Add suffix if configured
            if self.audio_config.say_all_clear_suffix:
                suffix_path = os.path.join(
                    self.audio_config.sounds_path,
                    self.audio_config.say_all_clear_suffix
                )
                suffix_audio = self.audio_processor.load_audio_file(suffix_path)
                if suffix_audio:
                    all_clear_audio += suffix_audio
            
            # Export audio file
            output_path = os.path.join("/tmp", "SkywarnPlus", "allclear.wav")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.audio_processor.export_audio(all_clear_audio, output_path):
                return False
            
            # Convert to Asterisk format
            if not self.asterisk_integration.convert_audio(output_path):
                return False
            
            # Send to nodes
            ulaw_path = output_path.replace('.wav', '.ulaw')
            return self.asterisk_integration.send_to_nodes(ulaw_path)
            
        except Exception as e:
            self.logger.error(f"Error announcing all clear: {e}")
            return False
    
    def build_tail_message(self, alerts: Dict[str, List[AlertData]]) -> bool:
        """Build and announce tail message."""
        try:
            # Generate tail message audio
            tail_audio = self._generate_tail_message_audio(alerts)
            if not tail_audio:
                self.logger.info("No tail message to announce")
                return True
            
            # Export audio file
            output_path = os.path.join("/tmp", "SkywarnPlus", "tailmessage.wav")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if not self.audio_processor.export_audio(tail_audio, output_path):
                return False
            
            # Convert to Asterisk format
            if not self.asterisk_integration.convert_audio(output_path):
                return False
            
            # Send to nodes
            ulaw_path = output_path.replace('.wav', '.ulaw')
            return self.asterisk_integration.send_to_nodes(ulaw_path)
            
        except Exception as e:
            self.logger.error(f"Error building tail message: {e}")
            return False
    
    def _generate_alert_audio(self, alert_type: str, alerts: List[AlertData]) -> Optional[Any]:
        """Generate audio for a specific alert type."""
        try:
            # Load alert sound
            alert_sound_path = os.path.join(
                self.audio_config.sounds_path,
                "ALERTS",
                self.audio_config.alert_sound
            )
            
            alert_sound = self.audio_processor.load_audio_file(alert_sound_path)
            if not alert_sound:
                return None
            
            # Start with alert sound
            audio_segments = [alert_sound]
            
            # Add silence
            silence = self.audio_processor.create_silence(600)
            if silence:
                audio_segments.append(silence)
            
            # Add alert type audio (this would need TTS integration)
            # For now, we'll add a placeholder
            
            # Add county names
            added_counties = set()
            for alert in alerts:
                county_code = alert.county_code
                if county_code in self.county_lookup and county_code not in added_counties:
                    county_config = self.county_lookup[county_code]
                    if county_config.wav_file:
                        county_path = os.path.join(
                            self.audio_config.sounds_path,
                            county_config.wav_file
                        )
                        county_audio = self.audio_processor.load_audio_file(county_path)
                        if county_audio:
                            audio_segments.append(county_audio)
                            added_counties.add(county_code)
            
            # Add alert separator
            separator_path = os.path.join(
                self.audio_config.sounds_path,
                "ALERTS",
                self.audio_config.alert_separator
            )
            separator = self.audio_processor.load_audio_file(separator_path)
            if separator:
                audio_segments.append(separator)
            
            return self.audio_processor.combine_audio(audio_segments)
            
        except Exception as e:
            self.logger.error(f"Error generating alert audio for {alert_type}: {e}")
            return None
    
    def _generate_tail_message_audio(self, alerts: Dict[str, List[AlertData]]) -> Optional[Any]:
        """Generate tail message audio."""
        try:
            audio_segments = []
            
            for alert_type, alert_list in alerts.items():
                # Add alert type
                # This would need TTS integration
                
                # Add counties
                added_counties = set()
                for alert in alert_list:
                    county_code = alert.county_code
                    if county_code in self.county_lookup and county_code not in added_counties:
                        county_config = self.county_lookup[county_code]
                        if county_config.wav_file:
                            county_path = os.path.join(
                                self.audio_config.sounds_path,
                                county_config.wav_file
                            )
                            county_audio = self.audio_processor.load_audio_file(county_path)
                            if county_audio:
                                audio_segments.append(county_audio)
                                added_counties.add(county_code)
                
                # Add separator between alerts
                separator_path = os.path.join(
                    self.audio_config.sounds_path,
                    "ALERTS",
                    self.audio_config.alert_separator
                )
                separator = self.audio_processor.load_audio_file(separator_path)
                if separator:
                    audio_segments.append(separator)
            
            return self.audio_processor.combine_audio(audio_segments) if audio_segments else None
            
        except Exception as e:
            self.logger.error(f"Error generating tail message audio: {e}")
            return None
