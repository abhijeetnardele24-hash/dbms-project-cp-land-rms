"""
Routes package initialization.
Imports all blueprint modules.
"""

from app.routes import auth, main, admin, registrar, officer, citizen, api, public, search

__all__ = ['auth', 'main', 'admin', 'registrar', 'officer', 'citizen', 'api', 'public', 'search']
