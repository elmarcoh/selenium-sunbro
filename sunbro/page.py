from sunbro.selectors import Selector


class PageMetaclass(type):
    """Metaclass that search for selenium selector objects on the
    class and makes them usable on the Page object
    """

    def __new__(cls, classname, bases, attrs):
        final_attrs = {}
        for k, v in attrs.iteritems():
            if isinstance(v, Selector):
                _k = '_' + k
                final_attrs[_k] = v
                final_attrs[k] = property(lambda s: getattr(s, _k).find(s.driver))
            else:
                final_attrs[k] = v

        return type.__new__(cls, classname, bases, final_attrs)


class Page:
    __metaclass__ = PageMetaclass

    def __init__(self, driver):
        self.driver = driver
