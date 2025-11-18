"""Tests for cereal-box-styles package."""

import pytest
from cereal_box_styles.server import OLOG_LOADER, CATEGORIES
from cereal_box_styles.tools import parse_prompt_components, apply_category_transformation


class TestOlogLoading:
    """Test that ologs load correctly."""
    
    def test_olog_loader_initialized(self):
        """Test that OlogLoader initializes without errors."""
        assert OLOG_LOADER is not None
        assert OLOG_LOADER.aesthetic_olog is not None
        assert OLOG_LOADER.intentionality_olog is not None
    
    def test_categories_loaded(self):
        """Test that categories are properly loaded."""
        assert CATEGORIES is not None
        assert len(CATEGORIES) == 7
        
        expected_categories = {
            'mascot_theater',
            'health_halo',
            'nostalgia_revival',
            'premium_disruptor',
            'kid_chaos',
            'transparent_honest',
            'adventure_fantasy'
        }
        assert set(CATEGORIES.keys()) == expected_categories
    
    def test_category_structure(self):
        """Test that each category has required structure."""
        required_fields = [
            'name',
            'description',
            'visual_dna',
            'ideal_subjects',
            'compatible_moods',
            'trigger_keywords',
            'core_intention'
        ]
        
        for category_name, category in CATEGORIES.items():
            for field in required_fields:
                assert field in category, f"{category_name} missing {field}"


class TestPromptParsing:
    """Test prompt parsing functionality."""
    
    def test_parse_simple_prompt(self):
        """Test parsing a simple prompt."""
        prompt = "a happy chef cooking soup"
        components = parse_prompt_components(prompt, OLOG_LOADER.get_transformation_maps())
        
        assert components is not None
        assert 'subject' in components
        assert 'action' in components
        assert 'setting' in components
        assert 'mood' in components
    
    def test_parse_subject_extraction(self):
        """Test that subjects are correctly extracted."""
        prompt = "a cheerful doctor"
        components = parse_prompt_components(prompt, OLOG_LOADER.get_transformation_maps())
        
        assert components['subject']['type'] == 'human'
        assert components['subject']['name'].lower() == 'doctor'
    
    def test_parse_action_extraction(self):
        """Test that actions are correctly extracted."""
        prompt = "a person running fast"
        components = parse_prompt_components(prompt, OLOG_LOADER.get_transformation_maps())
        
        assert components['action']['verb'] == 'running'
        assert components['action']['energy_level'] == 'high'


class TestTransformation:
    """Test aesthetic transformations."""
    
    def test_apply_transformation_mascot_theater(self):
        """Test mascot_theater transformation."""
        prompt = "a happy cat"
        components = parse_prompt_components(prompt, OLOG_LOADER.get_transformation_maps())
        
        transformed = apply_category_transformation(
            components,
            CATEGORIES['mascot_theater'],
            OLOG_LOADER.get_transformation_maps(),
            {}
        )
        
        assert transformed is not None
        assert 'subject' in transformed
    
    def test_apply_transformation_health_halo(self):
        """Test health_halo transformation."""
        prompt = "hands holding vegetables"
        components = parse_prompt_components(prompt, OLOG_LOADER.get_transformation_maps())
        
        transformed = apply_category_transformation(
            components,
            CATEGORIES['health_halo'],
            OLOG_LOADER.get_transformation_maps(),
            {}
        )
        
        assert transformed is not None
        assert 'colors' in transformed
    
    def test_all_categories_have_rules(self):
        """Test that all categories can apply transformations."""
        prompt = "a bird"
        components = parse_prompt_components(prompt, OLOG_LOADER.get_transformation_maps())
        
        for category_name, category_rules in CATEGORIES.items():
            transformed = apply_category_transformation(
                components,
                category_rules,
                OLOG_LOADER.get_transformation_maps(),
                {}
            )
            assert transformed is not None
            assert 'subject' in transformed
            assert 'colors' in transformed


class TestCategoryIntention:
    """Test that category intentions are properly specified."""
    
    def test_mascot_theater_intention(self):
        """Test mascot_theater has correct intention."""
        assert CATEGORIES['mascot_theater']['core_intention'] == 'playful_commercialism'
        assert 'joy' in CATEGORIES['mascot_theater']['composition_principle'].lower()
    
    def test_health_halo_intention(self):
        """Test health_halo has correct intention."""
        assert CATEGORIES['health_halo']['core_intention'] == 'authentic_naturalism'
        assert 'trust' in CATEGORIES['health_halo']['composition_principle'].lower()
    
    def test_all_categories_have_intention(self):
        """Test that all categories have core_intention and composition_principle."""
        for category_name, category in CATEGORIES.items():
            assert 'core_intention' in category, f"{category_name} missing core_intention"
            assert 'composition_principle' in category, f"{category_name} missing composition_principle"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
