import json

class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return {'__set__': True, 'values': tuple(obj)}
        return obj

class ExtendedJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        kwargs.setdefault('object_hook', self.object_hook)
        super().__init__(**kwargs)

    @staticmethod
    def object_hook(obj):
        if '__set__' in obj:
            return set(obj['values'])
        return obj