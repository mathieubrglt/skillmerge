"""SkillMerge: task-scoped composition of Agent Skills.

Index a skill library once into obligation/lesson atoms; return, per request, a single composite
skill scoped to one task and capped at a token budget. Composition on the request path is
deterministic and involves no model call.
"""
__version__ = "3.0.0"
