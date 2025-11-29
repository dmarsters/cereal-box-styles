# Cereal Box Styles

A categorical specification of 7 distinct cereal box design aesthetics using **ologs** (ontology logs from category theory). This package provides a formal framework for understanding, validating, and composing visual design systems.

## What Is This?

**Cereal Box Styles** transforms intuitive aesthetic knowledge into rigorous, composable, publishable specifications. Rather than hardcoding design rules, we use:

1. **Aesthetic Olog** - Categorical structure defining how visual elements (subjects, actions, settings, colors) compose into coherent styles
2. **Intentionality Olog** - Sensory and commercial reasoning explaining *why* each style works
3. **MCP Server** - Executable system that reads from the ologs to transform user prompts

This approach makes the system:
- **Verifiable** - Categorical structure is explicit and can be validated
- **Composable** - Can be combined with other aesthetic domains
- **Publishable** - YAML ologs can be cited, extended, and refined
- **Extensible** - Clear extension points for new categories

## The 7 Categories

| Category | Core Intent | Best For |
|----------|------------|----------|
| **Mascot Theater** | Playful joy through simple characters | Fun, energetic subjects |
| **Health Halo** | Authentic trust through minimalism | Wellness, natural products |
| **Nostalgia Revival** | Period-accurate comfort | Throwback, vintage feel |
| **Premium Disruptor** | Luxury through restraint | High-end, sophisticated |
| **Kid Chaos** | Excitement through sensory overload | Maximum energy, extreme fun |
| **Transparent Honest** | Clinical clarity and honesty | Educational, technical content |
| **Adventure Fantasy** | Wonder through mythologization | Epic, magical, heroic subjects |

## Installation

### From GitHub
```bash
pip install git+https://github.com/lushy/cereal-box-styles.git
```

### Local Development
```bash
git clone https://github.com/lushy/cereal-box-styles.git
cd cereal-box-styles
pip install -e .
```

### With Compiler Tools (Optional)
```bash
pip install -e ".[compiler]"
```

## Quick Start

### Using the MCP Server

```python
from cereal_box_styles.server import mcp

# The server is ready to use with Claude or other LLM interfaces
mcp.run()
```

### Programmatic Usage

```python
from cereal_box_styles.server import OLOG_LOADER, CATEGORIES
from cereal_box_styles.tools import parse_prompt_components, apply_transformations

# Parse a user prompt
user_prompt = "a playful chef tasting soup"
components = parse_prompt_components(user_prompt, OLOG_LOADER.get_transformation_maps())

# Apply mascot_theater transformation
transformed = apply_transformations(
    components,
    category="mascot_theater",
    style_params={"energy_level": 1.0}
)

print(transformed)
# Output: {'subject': '...', 'action': '...', 'colors': '...', ...}
```

### Getting Category Information

```python
from cereal_box_styles.server import mcp

# Get available categories
categories = mcp.get_available_categories()

# Get category details
rules = mcp.get_category_rules("mascot_theater")

# Get intentionality reasoning
intention = mcp.get_category_intention("health_halo")
```

## Understanding the Ologs

### The Aesthetic Olog (`cereal_box_styles.olog.yaml`)

Defines the categorical structure:

```yaml
types:
  Category:
    instances: [mascot_theater, health_halo, ...]
  SubjectType:
    instances: [human, animal, object, food, abstract]
  ActionEnergy:
    instances: [low_energy, medium_energy, high_energy]
  # ... and more

morphisms:
  - source: "Category + SubjectType"
    target: "SubjectTreatment"
    name: "subject_to_treatment"
    description: "Category transforms how subjects are depicted"

commutative_diagrams:
  category_coherence:
    assertion: "All visual choices must express the same category aesthetic"
    # ... paths and constraints
```

### The Intentionality Olog (`cereal_box_styles_intentionality.olog.yaml`)

Explains why each category works:

```yaml
instances:
  mascot_theater:
    core_intention: "playful_commercialism"
    composition_principle: "joy_through_simplification"
    why_this_works: |
      Every choice reinforces joy: cartoon style, bright colors,
      oversized proportions, motion lines. The stylization IS the promise.
```

## Tools

### Olog Compiler

Validate, visualize, and compile ologs:

```bash
# Validate olog structure
python -m cereal_box_styles.compiler validate cereal_box_styles.olog.yaml

# Generate Graphviz diagram
python -m cereal_box_styles.compiler diagram cereal_box_styles.olog.yaml --output cereal_box_styles.dot

# Convert to PNG
dot -Tpng cereal_box_styles.dot -o cereal_box_styles.png
```

## Architecture

```
cereal-box-styles/
├── cereal_box_styles/
│   ├── __init__.py
│   ├── server.py              # MCP server with OlogLoader
│   ├── data/
│   │   ├── ologs/
│   │   │   ├── cereal_box_styles.olog.yaml
│   │   │   └── cereal_box_styles_intentionality.olog.yaml
│   │   └── legacy/
│   │       ├── categories.json
│   │       ├── templates.json
│   │       └── transformation_maps.json
│   └── tools/
│       ├── parser.py
│       ├── transformer.py
│       └── utils.py
├── pyproject.toml
├── README.md
└── tests/
```

## How It Works

1. **User submits prompt** (e.g., "a playful chef")
2. **Parser extracts components** (subject: chef, mood: playful, etc.)
3. **Category selected** (e.g., mascot_theater)
4. **OlogLoader reads the olog** specifications
5. **Transformer applies morphisms** (transforms components according to category rules)
6. **Result returned** (enhanced prompt ready for image generation)

## Composition with Other Domains

The ologs are designed to compose with other aesthetic domains. For example:

- **Mascot Theater + Slapstick Comedy** (both use exaggeration and character)
- **Health Halo + Magazine Photography** (both use authentic, natural aesthetics)
- **Adventure Fantasy + Game Shows** (both use dramatic energy and visual spectacle)

To compose with another domain, identify shared categorical structure and implement the natural transformations defined in the ologs.

## Publishing and Extending

### For Researchers

The ologs are formal, publishable specifications:

```bibtex
@software{lushy-cereal-box-styles,
  title={Cereal Box Styles: A Categorical Specification of Visual Design Aesthetics},
  author={Lushy},
  year={2025},
  url={https://github.com/lushy/cereal-box-styles}
}
```

### Contributing

1. Fork the repository
2. Create a branch for your changes
3. Modify the YAML ologs and/or code
4. Run tests: `pytest`
5. Submit a pull request

When modifying ologs:
- Update the version in `pyproject.toml`
- Document your changes in the PR
- Ensure commutative diagram constraints are satisfied

## FAQ

**Q: What's an olog?**  
A: An ontology log—a formal specification from category theory that defines types, transformations (morphisms), and coherence constraints (commutative diagrams).

**Q: Why use ologs instead of just JSON?**  
A: Ologs are composable, formally verifiable, and can express constraints that JSON cannot. They're also designed to be human-readable and extendable.

**Q: Can I add new categories?**  
A: Yes! Add a new instance to the `Category` type in the aesthetic olog, define its morphisms and intentionality, and implement the transformation rules. The structure will guide you.

**Q: How do I compose with another aesthetic domain?**  
A: Create a similar olog for your domain, identify shared categorical structure (subject types, energy levels, etc.), and implement the natural transformations between them.

## Performance Considerations

- OlogLoader caches parsed specifications after first load
- Transformation pipeline is deterministic and fast
- MCP server maintains category cache for repeated use
- No external API calls required

## License

MIT License - see LICENSE file for details

## Related Projects

- **Lushy.app** - Full aesthetic systems platform
- **Slapstick Enhancer** - Categorical specification of slapstick comedy
- **Game Show Aesthetics** - Categorical specification of game show design
- **Magazine Photography** - Categorical specification of magazine aesthetics
- **Sanrio Character Builder** - Categorical specification of character design

## Contact

For questions, issues, or contributions:
- GitHub Issues: https://github.com/lushy/cereal-box-styles/issues
- Email: dal@lushy.app

## Author
Dal Marsters - Lushy.app
