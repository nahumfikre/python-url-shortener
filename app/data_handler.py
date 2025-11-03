import json
import os
import threading
import time
from typing import Optional, Dict


class UrlLogger:
    def __init__(self, log_path: str = 'data/links.log'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self._lock = threading.Lock()
        self._index: Dict[str, Dict] = {}
        self._load_log()

    def _load_log(self):
        if not os.path.exists(self.log_path):
            return
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get('op') == 'put':
                    self._index[rec['code']] = {
                        'url': rec['url'],
                        'expires_at': rec.get('expires_at'),
                        'created_at': rec.get('created_at', int(time.time()))
                    }

    def save(self, code: str, url: str, ttl_seconds: Optional[int] = None):
        now = int(time.time())
        expires_at = now + ttl_seconds if ttl_seconds else None
        rec = {
            'op': 'put',
            'code': code,
            'url': url,
            'created_at': now,
            'expires_at': expires_at
        }
        with self._lock:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(rec) + '\n')
            self._index[code] = {
                'url': url,
                'created_at': now,
                'expires_at': expires_at
            }

    def _is_expired(self, meta: Dict) -> bool:
        exp = meta.get('expires_at')
        return exp is not None and time.time() > exp

    def fetch(self, code: str) -> Optional[str]:
        # returns only the url (or None)
        meta = self._index.get(code)
        if not meta:
            return None
        if self._is_expired(meta):
            return None
        return meta['url']

    def peek(self, code: str) -> Optional[Dict]:
        # returns metadata for a code
        meta = self._index.get(code)
        if not meta:
            return None
        return {
            'code': code,
            'url': meta['url'],
            'created_at': meta['created_at'],
            'expires_at': meta['expires_at'],
            'expired': self._is_expired(meta)
        }
