"""
JSON Parser utility for extracting JSON from LLM responses.
Optimized with pre-compiled regex patterns for better performance.
"""
import json
import re
from typing import Dict, Any


class JSONParser:
    """Helper class to extract clean JSON from LLM responses."""
    
    # Pre-compile regex patterns for better performance
    _ANSWER_PATTERN = re.compile(r"<answer>\s*(.*?)\s*</answer>", re.DOTALL | re.IGNORECASE)
    _CODE_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
    _JSON_OBJECT_PATTERN = re.compile(r"(\{.*\})", re.DOTALL)
    
    @staticmethod
    def extract_json(text: str) -> Dict[str, Any]:
        """Attempts to extract a JSON block from text."""
        if not text:
            return {}
            
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # First, try to find JSON inside <answer> tags
        answer_match = JSONParser._ANSWER_PATTERN.search(text)
        if answer_match:
            answer_content = answer_match.group(1)
            # Try to find JSON in the answer content
            json_match = JSONParser._CODE_BLOCK_PATTERN.search(answer_content)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            # Try to find any JSON object in answer content
            json_match = JSONParser._JSON_OBJECT_PATTERN.search(answer_content)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
        
        # Fallback: try to find JSON in code blocks
        match = JSONParser._CODE_BLOCK_PATTERN.search(text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        # Fallback: try to find any JSON object
        match = JSONParser._JSON_OBJECT_PATTERN.search(text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return {}

