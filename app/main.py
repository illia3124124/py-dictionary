from __future__ import annotations
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.length = 8

    def pop(self, key: Any) -> Any:
        index = hash(key) % self.length
        for i in range(self.length):
            s_index = (index + i) % self.length
            if self.hash_table[s_index] is None:
                raise KeyError("Key not found")
            elif (self.hash_table[s_index][1] == hash(key)
                  and self.hash_table[s_index][0] == key):
                value = self.hash_table[s_index][2]
                self.hash_table[s_index] = None
                self._recreate()
                return value
        return None

    def update(self, updated_dict: dict) -> None:
        for key, value in updated_dict.items():
            index = hash(key) % self.length
            for i in range(self.length):
                s_index = (index + i) % self.length
                if self.hash_table[s_index] is None:
                    self.hash_table[s_index] = [key, hash(key), value]
                    break
                elif (self.hash_table[s_index][1] == hash(key)
                      and self.hash_table[s_index][0] == key):
                    self.hash_table[s_index][2] = value
                    break

    def get(self, key: Any) -> Any:
        index = hash(key) % self.length
        for i in range(self.length):
            s_index = (index + i) % self.length
            if self.hash_table[s_index] is None:
                raise KeyError("Key not found")
            elif self.hash_table[s_index][0] == key:
                return self.hash_table[s_index][2]
        raise KeyError("Key not found")

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 8

    def _resize(self) -> None:
        self.length *= 2
        self._recreate()

    def _recreate(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.length
        for idx in range(len(old_hash_table)):
            if old_hash_table[idx]:
                index = hash(old_hash_table[idx][0]) % self.length
                for i in range(len(self.hash_table)):
                    s_index = (index + i) % self.length
                    if self.hash_table[s_index] is None:
                        self.hash_table[s_index] = old_hash_table[idx]
                        break

    def __setitem__(self, key: Any, value: Any) -> None:
        if ((self.length - self.hash_table.count(None))
                / self.length >= (2 / 3)):
            self._resize()
        index = hash(key) % self.length
        for i in range(self.length):
            s_index = (index + i) % self.length
            if self.hash_table[s_index] is None:
                self.hash_table[s_index] = [key, hash(key), value]
                break
            elif (self.hash_table[s_index][1] == hash(key)
                  and self.hash_table[s_index][0] == key):
                self.hash_table[s_index][2] = value
                break

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.length
        for i in range(self.length):
            s_index = (index + i) % self.length
            if self.hash_table[s_index] is None:
                raise KeyError("Key not found")
            elif self.hash_table[s_index][0] == key:
                return self.hash_table[s_index][2]
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.length - self.hash_table.count(None)

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.length
        for i in range(self.length):
            s_index = (index + i) % self.length
            if self.hash_table[s_index] is None:
                return
            elif (self.hash_table[s_index][1] == hash(key)
                  and self.hash_table[s_index][0] == key):
                self.hash_table[s_index] = None
                self._recreate()
                break

    def __iter__(self) -> Dictionary:
        self._counter = -1
        return self

    def __next__(self) -> Any:
        self._counter += 1
        if self._counter >= self.length:
            raise StopIteration
        while self.hash_table[self._counter] is None:
            self._counter += 1
            if self._counter >= self.length:
                raise StopIteration
        return self.hash_table[self._counter][2]
