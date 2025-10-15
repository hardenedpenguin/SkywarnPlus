#!/usr/bin/env python3
"""
SkyDescribe - Text-to-Speech conversion for Weather Descriptions
Modernized version using the new modular architecture.
"""

import sys
import os
import logging
import argparse
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.config import ConfigManager
from src.tts_processor import TTSProcessor
from src.text_processor import TextProcessor
from src.state_manager import StateManager
from src.asterisk_integration import AsteriskIntegration
from src.exceptions import SkywarnPlusError


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('skydescribe.log')
        ]
    )


class SkyDescribe:
    """Main SkyDescribe application class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize SkyDescribe."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.state_manager = StateManager()
        self.tts_processor = TTSProcessor(self.config_manager)
        self.text_processor = TextProcessor()
        
        # Load configurations
        self.asterisk_config = self.config_manager.get_asterisk_config()
        self.asterisk_integration = AsteriskIntegration(self.asterisk_config)
        
        # Load state
        self.state = self.state_manager.load_state()
        
        self.logger.info("SkyDescribe initialized successfully")
    
    def find_alert_by_index_or_title(self, search_term: str) -> Optional[Dict]:
        """
        Find alert by index or title.
        
        Args:
            search_term: Index number or alert title to search for
            
        Returns:
            Alert data if found, None otherwise
        """
        try:
            # Try as index first
            if search_term.isdigit():
                index = int(search_term)
                alerts = self.state.get("last_alerts", {})
                alert_list = list(alerts.items())
                
                if 0 <= index < len(alert_list):
                    alert_type, alert_data = alert_list[index]
                    return {
                        "type": alert_type,
                        "data": alert_data,
                        "index": index
                    }
            
            # Search by title
            alerts = self.state.get("last_alerts", {})
            for alert_type, alert_data in alerts.items():
                if search_term.lower() in alert_type.lower():
                    return {
                        "type": alert_type,
                        "data": alert_data,
                        "index": None
                    }
            
            self.logger.warning(f"Alert not found: {search_term}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding alert: {e}")
            return None
    
    def generate_description_audio(self, alert_info: Dict) -> bool:
        """
        Generate audio for alert description.
        
        Args:
            alert_info: Alert information dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            alert_type = alert_info["type"]
            alert_data = alert_info["data"]
            
            # Get description from first alert in the list
            if not alert_data:
                self.logger.error("No alert data available")
                return False
            
            first_alert = alert_data[0] if isinstance(alert_data, list) else alert_data
            description = first_alert.get("description", "")
            
            if not description:
                self.logger.warning(f"No description available for {alert_type}")
                return False
            
            # Generate filename
            filename = self.text_processor.sanitize_for_filename(alert_type)
            output_file = f"/tmp/SkywarnPlus/{filename}_description.wav"
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Convert to audio
            success = self.tts_processor.convert_to_audio(description, output_file)
            
            if success:
                self.logger.info(f"Generated description audio: {output_file}")
                
                # Convert to Asterisk format
                ulaw_file = output_file.replace('.wav', '.ulaw')
                if self.asterisk_integration.convert_audio(output_file):
                    self.logger.info(f"Converted to ULAW: {ulaw_file}")
                    return True
                else:
                    self.logger.error("Failed to convert to ULAW format")
                    return False
            else:
                self.logger.error("Failed to generate description audio")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating description audio: {e}")
            return False
    
    def run(self, search_term: str) -> bool:
        """
        Run SkyDescribe with the given search term.
        
        Args:
            search_term: Index or title to search for
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find the alert
            alert_info = self.find_alert_by_index_or_title(search_term)
            if not alert_info:
                self.logger.error(f"Alert not found: {search_term}")
                return False
            
            # Generate audio
            success = self.generate_description_audio(alert_info)
            
            if success:
                self.logger.info(f"Successfully processed alert: {alert_info['type']}")
                return True
            else:
                self.logger.error("Failed to generate audio")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in SkyDescribe run: {e}")
            return False


def main():
    """Main entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SkyDescribe - Weather Alert TTS")
    parser.add_argument("index_or_title", help="Alert index or title to process")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    try:
        with SkyDescribe(args.config) as app:
            success = app.run(args.index_or_title)
            sys.exit(0 if success else 1)
            
    except SkywarnPlusError as e:
        logger.error(f"SkyDescribe error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
