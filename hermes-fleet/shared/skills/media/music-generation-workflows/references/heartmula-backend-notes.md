# HeartMuLa Backend Notes

This reference preserves backend-specific operational detail under the music-generation umbrella.

## Class
Open-source lyrics-plus-tags song generation backend.

## Keep in reference form because
The content is valuable, but it is backend-specific support material rather than a separate top-level skill class.

## Operational notes
- Verify Python version compatibility before install.
- Verify VRAM budget before model download and generation.
- Use a smallest possible generation first to validate the pipeline.
- Track dependency and checkpoint quirks here, not in a separate sibling skill.

## Typical concerns
- dependency pin drift
- transformer/version incompatibilities
- checkpoint layout expectations
- codec/model memory split
- generation duration/runtime trade-offs
