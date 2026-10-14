import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from app import load_tasks, save_tasks


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "nested" / "tasks.json"
        self.tasks = [{"id": "a", "title": "Learn Python — practice", "done": False}]

    def test_save_reload_and_complete(self):
        self.assertEqual(load_tasks(self.path), [])
        save_tasks(self.path, self.tasks)
        self.assertEqual(load_tasks(self.path), self.tasks)
        self.tasks[0]["done"] = True
        save_tasks(self.path, self.tasks)
        self.assertTrue(load_tasks(self.path)[0]["done"])

    def test_failed_replacement_preserves_previous_save(self):
        save_tasks(self.path, self.tasks)
        previous = self.path.read_bytes()
        with patch("app.os.replace", side_effect=OSError("Disk unavailable")):
            with self.assertRaises(OSError):
                save_tasks(self.path, [])
        self.assertEqual(self.path.read_bytes(), previous)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_saved_data_is_rejected_and_preserved(self):
        self.path.parent.mkdir()
        for data in ({}, [{"id": "a", "title": "Task", "done": "false"}], self.tasks * 2):
            content = json.dumps(data)
            self.path.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tasks(self.path)
            self.assertEqual(self.path.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()
