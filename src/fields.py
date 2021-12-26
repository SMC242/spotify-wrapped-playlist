from typing import List, Union


class Fields:
    """Wraps a set of fields for a spotify request.

    Examples:
        ?fields=collaberative,description,external_urls
        -> Fields("collaberative" ,"description", "external_urls")

        ?fields=followers,items(added_at,album(name,href))
        -> Fields("followers", Fields(Fields("name", "href", title="album"), title="items"))
    """

    def __init__(self, *fields: Union[str, 'Fields'], title: str = None):
        self.fields = fields
        self.title = title

    def construct(self):
        """Join together all of the fields, including subfields."""
        constructed = map(lambda f: f.construct() if not isinstance(
            f, str) else f, self.fields)
        joined = ','.join(constructed)
        return f"{self.title}({joined})" if self.title else joined

    def query(self):
        """Create the query string."""
        return f"fields={self.construct()}"
