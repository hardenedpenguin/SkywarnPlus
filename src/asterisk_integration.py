"""
Asterisk integration functionality for SkywarnPlus.
"""

import logging
import subprocess
import time
from typing import Dict, Any, Optional, List

from .exceptions import ValidationError
from .data_types import AsteriskConfig


class AsteriskIntegration:
    """Handles Asterisk integration for radio repeater systems."""
    
    def __init__(self, config: AsteriskConfig):
        """Initialize Asterisk integration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def convert_audio(self, audio_file: str) -> bool:
        """Convert audio file to Asterisk-compatible format."""
        try:
            # Convert WAV to ULAW format for Asterisk
            output_file = audio_file.replace('.wav', '.ulaw')
            
            result = subprocess.run(
                ['sox', audio_file, '-t', 'ulaw', '-r', '8000', output_file],
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )
            
            if result.returncode == 0:
                self.logger.debug(f"Converted audio: {audio_file} -> {output_file}")
                return True
            else:
                self.logger.error(f"Audio conversion failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Audio conversion timed out")
            return False
        except Exception as e:
            self.logger.error(f"Audio conversion error: {e}")
            return False
    
    def change_ct(self, mode: str) -> bool:
        """Change control tone mode."""
        try:
            # Build asterisk command
            cmd = ['asterisk', '-rx', f'rpt setct {mode}']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result.returncode == 0:
                self.logger.debug(f"Control tone changed to: {mode}")
                return True
            else:
                self.logger.error(f"Control tone change failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Control tone change timed out")
            return False
        except Exception as e:
            self.logger.error(f"Control tone change error: {e}")
            return False
    
    def change_id(self, node_id: str) -> bool:
        """Change node ID."""
        try:
            # Build asterisk command
            cmd = ['asterisk', '-rx', f'rpt setid {node_id}']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result.returncode == 0:
                self.logger.debug(f"Node ID changed to: {node_id}")
                return True
            else:
                self.logger.error(f"Node ID change failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Node ID change timed out")
            return False
        except Exception as e:
            self.logger.error(f"Node ID change error: {e}")
            return False
    
    def send_to_nodes(self, audio_file: str, nodes: Optional[List[int]] = None) -> bool:
        """Send audio file to specified nodes."""
        if nodes is None:
            nodes = self.config.nodes
        
        if not nodes:
            self.logger.warning("No nodes configured")
            return False
        
        success_count = 0
        
        for node in nodes:
            try:
                # Build asterisk command for each node
                cmd = ['asterisk', '-rx', f'rpt play {node} {audio_file}']
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False
                )
                
                if result.returncode == 0:
                    self.logger.debug(f"Sent audio to node {node}")
                    success_count += 1
                else:
                    self.logger.error(f"Failed to send to node {node}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                self.logger.error(f"Timeout sending to node {node}")
            except Exception as e:
                self.logger.error(f"Error sending to node {node}: {e}")
        
        return success_count == len(nodes)
    
    def update_asterisk_variables(self, variables: Dict[str, Any]) -> bool:
        """Update Asterisk variables."""
        try:
            for var_name, var_value in variables.items():
                cmd = ['asterisk', '-rx', f'setvar {var_name} {var_value}']
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False
                )
                
                if result.returncode != 0:
                    self.logger.error(f"Failed to set variable {var_name}: {result.stderr}")
                    return False
            
            self.logger.debug("Asterisk variables updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating Asterisk variables: {e}")
            return False
