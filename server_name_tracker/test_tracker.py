import unittest

from server_name_tracker.main.tracker_practice import SilentTracker, NonSilentTracker


class TestTrackers(unittest.TestCase):
    def test_allocate_basic(self):
        t = SilentTracker()
        self.assertEqual(t.allocate("api"), "api1")
        self.assertEqual(t.allocate("api"), "api2")
        self.assertEqual(t.allocate("web"), "web1")
        self.assertEqual(t.allocate("web"), "web2")

    def test_reuse_smallest(self):
        t = SilentTracker()
        self.assertEqual(t.allocate("api"), "api1")
        self.assertEqual(t.allocate("api"), "api2")
        t.deallocate("api1")
        self.assertEqual(t.allocate("api"), "api1")  # reuse freed smallest
        self.assertEqual(t.allocate("api"), "api3")  # next new id

    def test_per_type_independent(self):
        t = SilentTracker()
        self.assertEqual(t.allocate("api"), "api1")
        self.assertEqual(t.allocate("web"), "web1")
        t.deallocate("api1")
        self.assertEqual(t.allocate("web"), "web2")
        self.assertEqual(t.allocate("api"), "api1")

    def test_silent_invalid_deallocate_noop(self):
        t = SilentTracker()
        t.deallocate("api1")  # never allocated -> no-op
        t.deallocate("api01")  # malformed -> no-op
        t.allocate("api")  # should still work
        t.deallocate("api2")  # invalid -> no-op

    def test_nonsilent_invalid_deallocate_raises(self):
        t = NonSilentTracker()
        t.allocate("api")
        with self.assertRaises(Exception) as ctx:
            t.deallocate("api2")
        self.assertIn("Invalid Operation", str(ctx.exception))

    def test_double_free_behavior(self):
        t = NonSilentTracker()
        self.assertEqual(t.allocate("api"), "api1")
        t.deallocate("api1")
        with self.assertRaises(Exception):
            t.deallocate("api1")  # second deallocate invalid

    def test_malformed_hostname_raises(self):
        t = NonSilentTracker()
        with self.assertRaises(Exception):
            t.deallocate("api")  # no number
        with self.assertRaises(Exception):
            t.deallocate("api0")  # zero not allowed
        with self.assertRaises(Exception):
            t.deallocate("api01")  # leading zero not allowed


if __name__ == "__main__":
    unittest.main()
