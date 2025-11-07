"""
Semantic Cache System for PSUR Document Parsing
Provides persistent caching of parsed CER semantic data to avoid repeated API calls.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class SemanticCERCache:
    """
    Persistent cache for parsed CER semantic data.
    Stores parsed CER models to avoid repeated Anthropic API calls.
    
    Cache Strategy:
    - Cache key based on file path + modification time + size
    - Automatic invalidation when source file changes
    - JSON serialization for portability
    - Optional compression for large documents
    """
    
    def __init__(self, cache_dir: str = None):
        """
        Initialize semantic cache.
        
        Args:
            cache_dir: Directory for cache storage. Defaults to .semantic_cache in project root.
        """
        if cache_dir is None:
            # Default to .semantic_cache in project root
            project_root = Path(__file__).parent.parent
            cache_dir = project_root / '.semantic_cache'
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize metadata file
        self.metadata_file = self.cache_dir / 'metadata.json'
        self._init_metadata()
    
    def _init_metadata(self):
        """Initialize or load cache metadata"""
        if not self.metadata_file.exists():
            metadata = {
                'created': datetime.now().isoformat(),
                'version': '1.0',
                'cache_entries': {}
            }
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
    
    def get_cache_key(self, file_path: str) -> str:
        """
        Generate cache key from file path + modification time + size.
        
        Args:
            file_path: Path to source document
            
        Returns:
            MD5 hash serving as cache key
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = os.stat(file_path)
        
        # Create unique identifier from path, mtime, and size
        cache_string = f"{os.path.abspath(file_path)}_{stat.st_mtime}_{stat.st_size}"
        
        cache_key = hashlib.md5(cache_string.encode()).hexdigest()
        
        return cache_key
    
    def save(self, file_path: str, data: Dict[str, Any], doc_type: str = 'cer'):
        """
        Save parsed document data to cache.
        
        Args:
            file_path: Original document path
            data: Parsed semantic data (must be JSON-serializable)
            doc_type: Document type ('cer', 'psur', etc.)
        """
        cache_key = self.get_cache_key(file_path)
        cache_file = self.cache_dir / f"{cache_key}_{doc_type}.json"
        
        # Prepare cache entry
        cache_entry = {
            'file_path': os.path.abspath(file_path),
            'doc_type': doc_type,
            'cached_at': datetime.now().isoformat(),
            'cache_key': cache_key,
            'data': data
        }
        
        # Save to cache file
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_entry, f, indent=2, default=str, ensure_ascii=False)
        
        # Update metadata
        self._update_metadata(cache_key, file_path, doc_type)
        
        try:
            print(f"  \u2713 Cached semantic data: {cache_file.name}")
        except:
            print(f"  Cached semantic data: {cache_file.name}")
    
    def load(self, file_path: str, doc_type: str = 'cer') -> Optional[Dict[str, Any]]:
        """
        Load cached document data if available and valid.
        
        Args:
            file_path: Original document path
            doc_type: Document type ('cer', 'psur', etc.)
            
        Returns:
            Cached data dict or None if not found/invalid
        """
        try:
            cache_key = self.get_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}_{doc_type}.json"
            
            if not cache_file.exists():
                return None
            
            # Load cache entry
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_entry = json.load(f)
            
            # Validate cache entry
            if cache_entry.get('cache_key') != cache_key:
                print(f"  Warning: Cache key mismatch, invalidating cache")
                return None
            
            try:
                print(f"  \u2713 Found semantic cache (from {cache_entry.get('cached_at', 'unknown')})")
            except:
                print(f"  Found semantic cache (from {cache_entry.get('cached_at', 'unknown')})")
            
            return cache_entry.get('data')
            
        except Exception as e:
            print(f"  Warning: Could not load cache: {e}")
            return None
    
    def exists(self, file_path: str, doc_type: str = 'cer') -> bool:
        """
        Check if valid cache exists for file.
        
        Args:
            file_path: Original document path
            doc_type: Document type
            
        Returns:
            True if valid cache exists
        """
        try:
            cache_key = self.get_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}_{doc_type}.json"
            return cache_file.exists()
        except:
            return False
    
    def invalidate(self, file_path: str, doc_type: str = 'cer'):
        """
        Invalidate cache for specific file.
        
        Args:
            file_path: Original document path
            doc_type: Document type
        """
        try:
            cache_key = self.get_cache_key(file_path)
            cache_file = self.cache_dir / f"{cache_key}_{doc_type}.json"
            
            if cache_file.exists():
                cache_file.unlink()
                print(f"  ✓ Invalidated cache for {file_path}")
            
            # Update metadata
            self._remove_from_metadata(cache_key)
            
        except Exception as e:
            print(f"  Warning: Could not invalidate cache: {e}")
    
    def clean_old_caches(self, max_age_days: int = 30):
        """
        Remove cache files older than specified days.
        
        Args:
            max_age_days: Maximum age in days before cache is removed
        """
        count = 0
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_days * 24 * 60 * 60
        
        for cache_file in self.cache_dir.glob('*.json'):
            if cache_file.name == 'metadata.json':
                continue
            
            file_age = current_time - cache_file.stat().st_mtime
            
            if file_age > max_age_seconds:
                cache_file.unlink()
                count += 1
        
        if count > 0:
            print(f"  ✓ Cleaned {count} old cache files")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache stats (count, total size, etc.)
        """
        cache_files = list(self.cache_dir.glob('*.json'))
        cache_files = [f for f in cache_files if f.name != 'metadata.json']
        
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'cache_count': len(cache_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir),
            'files': [f.name for f in cache_files]
        }
    
    def _update_metadata(self, cache_key: str, file_path: str, doc_type: str):
        """Update metadata file with new cache entry"""
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            metadata['cache_entries'][cache_key] = {
                'file_path': file_path,
                'doc_type': doc_type,
                'cached_at': datetime.now().isoformat()
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"  Warning: Could not update metadata: {e}")
    
    def _remove_from_metadata(self, cache_key: str):
        """Remove entry from metadata"""
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            if cache_key in metadata.get('cache_entries', {}):
                del metadata['cache_entries'][cache_key]
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"  Warning: Could not update metadata: {e}")


class SemanticParserSession:
    """
    Session-level cache for semantic parser.
    Provides in-memory caching for current execution session.
    
    Usage:
        cer_data = SemanticParserSession.get_cer_data(cer_path)
        # Subsequent calls return cached data instantly
    """
    
    # Class-level session cache
    _session_cache: Dict[str, Dict[str, Any]] = {}
    _disk_cache = SemanticCERCache()
    
    @classmethod
    def get_cer_data(cls, cer_path: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get CER data from session cache, disk cache, or parse if needed.
        
        Args:
            cer_path: Path to CER document
            force_refresh: Force re-parsing even if cached
            
        Returns:
            Parsed CER data dict
        """
        cache_key = f"cer_{os.path.abspath(cer_path)}"
        
        # Check session cache first (fastest)
        if not force_refresh and cache_key in cls._session_cache:
            return cls._session_cache[cache_key]
        
        # Check disk cache (fast)
        if not force_refresh:
            cached_data = cls._disk_cache.load(cer_path, doc_type='cer')
            if cached_data:
                cls._session_cache[cache_key] = cached_data
                return cached_data
        
        # Need to parse - this will be done by semantic parser
        # For now, return None to trigger parsing
        return None
    
    @classmethod
    def set_cer_data(cls, cer_path: str, data: Dict[str, Any]):
        """
        Store CER data in session and disk cache.
        
        Args:
            cer_path: Path to CER document
            data: Parsed CER data
        """
        cache_key = f"cer_{os.path.abspath(cer_path)}"
        
        # Store in session cache
        cls._session_cache[cache_key] = data
        
        # Store in disk cache
        cls._disk_cache.save(cer_path, data, doc_type='cer')
    
    @classmethod
    def clear_session(cls):
        """Clear session cache (not disk cache)"""
        cls._session_cache.clear()
        print("  ✓ Cleared session cache")
    
    @classmethod
    def get_session_stats(cls) -> Dict[str, Any]:
        """Get session cache statistics"""
        return {
            'session_entries': len(cls._session_cache),
            'cached_files': list(cls._session_cache.keys())
        }

