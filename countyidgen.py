#!/usr/bin/env python3
"""
CountyIDGen - County ID audio file generator
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
from src.county_id_generator import CountyIDGenerator
from src.exceptions import SkywarnPlusError


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('countyidgen.log')
        ]
    )


class CountyIDGenApp:
    """Main CountyIDGen application class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize CountyIDGen application."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.county_generator = CountyIDGenerator(self.config_manager)
        
        # Load configurations
        self.audio_config = self.config_manager.get_audio_config()
        self.county_configs = self.config_manager.get_county_configs()
        
        self.logger.info("CountyIDGen initialized successfully")
    
    def display_warning(self) -> bool:
        """Display warning and get user confirmation."""
        warning_msg = """
⚠️  WARNING: County ID Audio Generation ⚠️

This script will generate WAV audio files for each county code in your configuration.
This process will:
- Make API calls to VoiceRSS (may incur costs)
- Generate audio files in your SOUNDS directory
- Backup existing WAV files before overwriting

Do you want to continue? (y/N): """
        
        try:
            response = input(warning_msg).strip().lower()
            return response in ['y', 'yes']
        except KeyboardInterrupt:
            self.logger.info("Operation cancelled by user")
            return False
    
    def load_county_data(self) -> Dict[str, str]:
        """Load county data from CountyCodes.md file."""
        county_codes_path = os.path.join(os.path.dirname(__file__), "CountyCodes.md")
        
        if not os.path.exists(county_codes_path):
            self.logger.error(f"CountyCodes.md not found at: {county_codes_path}")
            return {}
        
        return self.county_generator.load_county_codes_from_md(county_codes_path)
    
    def run(self, force: bool = False) -> bool:
        """
        Run the county ID generation process.
        
        Args:
            force: Skip confirmation prompt
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate configuration
            if not self.county_generator.validate_config():
                self.logger.error("Configuration validation failed")
                return False
            
            # Check if we have county codes
            if not self.county_configs:
                self.logger.error("No county codes configured")
                return False
            
            # Display warning unless forced
            if not force and not self.display_warning():
                self.logger.info("Operation cancelled by user")
                return False
            
            # Load county data
            county_data = self.load_county_data()
            if not county_data:
                self.logger.error("Failed to load county data")
                return False
            
            # Process county codes
            sounds_path = self.audio_config.sounds_path
            success = self.county_generator.process_county_codes(
                self.county_configs, sounds_path, county_data
            )
            
            if success:
                self.logger.info("County ID generation completed successfully!")
                self.logger.info(f"Audio files saved to: {sounds_path}")
                return True
            else:
                self.logger.error("County ID generation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in CountyIDGen run: {e}")
            return False


def main():
    """Main entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CountyIDGen - Generate county audio files")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--force", action="store_true", 
                       help="Skip confirmation prompt")
    
    args = parser.parse_args()
    
    try:
        with CountyIDGenApp(args.config) as app:
            success = app.run(force=args.force)
            sys.exit(0 if success else 1)
            
    except SkywarnPlusError as e:
        logger.error(f"CountyIDGen error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
