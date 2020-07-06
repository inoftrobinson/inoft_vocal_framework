class DummyObject:
    # When we try to access any attribute of the
    # dummy object, it will return himself.
    def __getattr__(self, item):
        return self

    # And if dummy object is called, nothing is being done,
    # and error created if the function did not exist.
    def __call__(self, *args, **kwargs):
        pass

dummy_object = DummyObject()

