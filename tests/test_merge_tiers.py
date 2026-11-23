import sys
sys.path.append("src")
import os, json
from merge_tiers import unify_tier

def test_unify_tier_changed():
    assert unify_tier("ag") == "uber"

def test_unify_tier_unchanged():
    assert unify_tier("ou") == "ou"