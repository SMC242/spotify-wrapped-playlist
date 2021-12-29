import unittest

from src.formatting.fields import Fields


class TestFields(unittest.TestCase):
    def test_fields(self):
        fs = Fields("eggs", "ham", "spam")
        self.assertEqual("eggs,ham,spam", fs.construct())

    def test_subfield(self):
        # In the context of a school class' members
        fs = Fields(Fields("id", "name", "phone_number", title="members"))
        self.assertEqual("members(id,name,phone_number)", fs.construct())

    def test_mixed(self):
        fs = Fields("name", "age", Fields("name", "age", title="pets"))
        self.assertEqual("name,age,pets(name,age)", fs.construct())

    def test_nested(self):
        fs = Fields(Fields("name", "age", Fields(
            "street", "city", title="address"), title="person"))
        self.assertEqual(
            "person(name,age,address(street,city))", fs.construct())


if __name__ == '__main__':
    unittest.main()
