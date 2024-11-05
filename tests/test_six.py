import unittest
import sys
import types
import io

import ten99policy.six as six


class TestSix(unittest.TestCase):

    def test_python_version(self):
        self.assertIn(six.PY2, [True, False])
        self.assertIn(six.PY3, [True, False])
        self.assertNotEqual(six.PY2, six.PY3)

    def test_string_types(self):
        if six.PY3:
            self.assertEqual(six.string_types, (str,))
        else:
            self.assertEqual(six.string_types, (basestring,))

    def test_integer_types(self):
        if six.PY3:
            self.assertEqual(six.integer_types, (int,))
        else:
            self.assertEqual(six.integer_types, (int, long))

    def test_class_types(self):
        if six.PY3:
            self.assertEqual(six.class_types, (type,))
        else:
            self.assertEqual(six.class_types, (type, types.ClassType))

    def test_text_type(self):
        if six.PY3:
            self.assertEqual(six.text_type, str)
        else:
            self.assertEqual(six.text_type, unicode)

    def test_binary_type(self):
        if six.PY3:
            self.assertEqual(six.binary_type, bytes)
        else:
            self.assertEqual(six.binary_type, str)

    def test_maxsize(self):
        self.assertEqual(six.MAXSIZE, sys.maxsize)

    def test_b(self):
        self.assertEqual(six.b("foo"), b"foo")

    def test_u(self):
        self.assertEqual(six.u("foo"), "foo")

    def test_unichr(self):
        self.assertEqual(six.unichr(97), "a")

    def test_int2byte(self):
        self.assertEqual(six.int2byte(65), b"A")

    def test_byte2int(self):
        self.assertEqual(six.byte2int(b"A"), 65)

    def test_indexbytes(self):
        self.assertEqual(six.indexbytes(b"ABC", 1), 66)

    def test_iterbytes(self):
        self.assertEqual(list(six.iterbytes(b"ABC")), [65, 66, 67])

    def test_StringIO(self):
        self.assertTrue(isinstance(six.StringIO(), io.StringIO))

    def test_BytesIO(self):
        self.assertTrue(isinstance(six.BytesIO(), io.BytesIO))

    def test_exec_(self):
        namespace = {}
        six.exec_("a = 1", namespace)
        self.assertEqual(namespace["a"], 1)

    def test_reraise(self):
        try:
            try:
                raise ValueError("test")
            except ValueError:
                six.reraise(*sys.exc_info())
        except ValueError as e:
            self.assertEqual(str(e), "test")

    def test_raise_from(self):
        try:
            six.raise_from(ValueError("test"), TypeError("original"))
        except ValueError as e:
            self.assertEqual(str(e), "test")
            if six.PY3:
                self.assertIsInstance(e.__cause__, TypeError)

    def test_print_(self):
        buf = six.StringIO()
        six.print_("Hello", "world!", file=buf)
        self.assertEqual(buf.getvalue().strip(), "Hello world!")

    def test_with_metaclass(self):
        class Meta(type):
            pass

        class Base(object):
            pass

        class MyClass(six.with_metaclass(Meta, Base)):
            pass

        self.assertTrue(isinstance(MyClass, Meta))
        self.assertTrue(issubclass(MyClass, Base))

    def test_add_metaclass(self):
        class Meta(type):
            pass

        @six.add_metaclass(Meta)
        class MyClass(object):
            pass

        self.assertTrue(isinstance(MyClass, Meta))

    def test_python_2_unicode_compatible(self):
        @six.python_2_unicode_compatible
        class MyClass(object):
            def __str__(self):
                return "unicode"

        self.assertEqual(str(MyClass()), "unicode")
        if six.PY2:
            self.assertTrue(hasattr(MyClass, "__unicode__"))

    def test_wraps(self):
        def decorator(func):
            @six.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        @decorator
        def example():
            """Docstring"""
            pass

        self.assertEqual(example.__name__, "example")
        self.assertEqual(example.__doc__, "Docstring")

    def test_iterkeys(self):
        d = {"a": 1, "b": 2}
        self.assertEqual(list(six.iterkeys(d)), ["a", "b"])

    def test_itervalues(self):
        d = {"a": 1, "b": 2}
        self.assertEqual(list(six.itervalues(d)), [1, 2])

    def test_iteritems(self):
        d = {"a": 1, "b": 2}
        self.assertEqual(list(six.iteritems(d)), [("a", 1), ("b", 2)])

    def test_callable(self):
        def func():
            pass

        self.assertTrue(six.callable(func))
        self.assertFalse(six.callable(1))


if __name__ == "__main__":
    unittest.main()
