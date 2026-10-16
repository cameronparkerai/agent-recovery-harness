"""Hash-chained audit log for experiment bookkeeping: separates what the
environment committed from what an agent *believes* it committed.

Not a security boundary. verify() only checks internal consistency; no trusted
digest is kept outside the log, so a party that can rewrite the whole chain (or
drop its tail) is not detected."""
import copy
import hashlib
import json


class TamperError(Exception):
    pass


class EventLog:
    def __init__(self):
        self._entries = []

    @staticmethod
    def _digest(prev, payload):
        blob = json.dumps({"prev": prev, "payload": payload}, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()

    def append(self, payload):
        payload = copy.deepcopy(payload)
        prev = self._entries[-1]["hash"] if self._entries else "genesis"
        self._entries.append({"payload": payload, "hash": self._digest(prev, payload)})

    def verify(self):
        """Return deep copies of the payloads if the chain is internally
        consistent, else raise TamperError. Callers cannot mutate the log
        through the returned objects."""
        prev = "genesis"
        for i, e in enumerate(self._entries):
            if e["hash"] != self._digest(prev, e["payload"]):
                raise TamperError(f"entry {i} fails hash check")
            prev = e["hash"]
        return [copy.deepcopy(e["payload"]) for e in self._entries]
