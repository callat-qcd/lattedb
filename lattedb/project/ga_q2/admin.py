"""Admin pages for ga_q2 models

On default generates list view admins for all models
"""
from espressodb.base.admin import register_admins

register_admins("lattedb.project.ga_q2")
