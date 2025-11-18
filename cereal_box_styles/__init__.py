"""
Cereal Box Styles - Categorical Specification of Visual Design Aesthetics

A formal specification system using ologs (categorical ontology language)
to define how different cereal box design aesthetics compose visual elements.

Provides:
- Categorical structure of 7 distinct design styles
- Sensory intentionality reasoning for each style
- MCP server for aesthetic transformation
- Tools for composing with other aesthetic domains
"""

__version__ = "1.0.0"
__author__ = "Lushy"
__description__ = "Categorical specification of cereal box design aesthetics"

from .server import mcp

__all__ = ["mcp"]
