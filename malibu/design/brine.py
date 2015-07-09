import pdb
import difflib, json, time, types, uuid
from difflib import SequenceMatcher

""" Brine is a play on Python's pickle module, which is used for
    serializing data. Brine is used for serialization as well, but
    into JSON, not a binary structure.
"""


def fuzzy_ratio(a, b):
    """ Compares two values using the SequenceMatcher from difflib.
        Used for ~approximated~ fuzzy search.
    """

    return SequenceMatcher(None, a, b).ratio()


class BrineState(object):
    """ This class is for meta-class use as a semi-state machine.
        It provides a sort of persistence with searchable fields,
        which should end up operating similar to the DBMapper, but
        without the database.

        The end-goal for this JSON model is to be able to provide
        an interface for a class that will serialize easily to JSON
        to go into a datastore (such as MongoDB) and be searchable
        without ties back to the database itself.

        Each class that implements the JsonModelledState will maintain
        a class scoped list of instances that will be used for searching
        and maintaining a sort of cache that can be modified before the
        contents get serialized and stored in a database.

        Eventually, a subclass may appear within this module which provides
        cache expiry on items, or at least a time-based flag which can signal
        that a data set that is stored in one of these objects is `dirty`.
    """

    # Ratio for fuzzy search. Closer to 1.0 means stricter results.
    _FUZZ_RATIO = 0.535

    @classmethod
    def __initialize_cache(cls):
        """ Initialize a class-level cache to store Json models for cache and
            searching purposes.
        """

        if not hasattr(cls, "_BrineState__cache"):
            cls.__cache = []

    @classmethod
    def fuzzy_search(cls, ignore_case = False, **kw):
        """ Performs a fuzzy search on the cache to find objects that have at
            least a diff ratio of FUZZ_RATIO.

            Note that this can return more than one object and it may not be
            accurate. Time will tell.

            Returns a list of matches ordered by likelihood of match.
        """

        ratios = {}

        for k, v in kw.iteritems():
            for obj in cls.__cache:
                ob_value = getattr(obj, k, None)
                if ignore_case:
                    if isinstance(v, str) and isinstance(ob_value, str):
                        r = fuzzy_ratio(ob_value.lower(), v.lower())
                else:
                    r = fuzzy_ratio(ob_value, v)
                if r >= cls._FUZZ_RATIO:
                    ratios.update({obj: r})

        # TODO - sort by fuzzy search ratio.
        # We need to ensure the results get properly sorted by match ratio
        # before returning.

        return ratios.keys()

    @classmethod
    def search(cls, ignore_case = False, **kw):
        """ Searches through the cache to find objects with field that match
            those given by the **kw.

            Note that this can return more than one object.
        """

        result = []

        for k, v in kw.iteritems():
            for obj in cls.__cache:
                ob_value = getattr(obj, k, None)
                if ignore_case:
                    if isinstance(v, str) and isinstance(ob_value, str):
                        r = (v.lower() == ob_value.lower())
                else:
                    r = (v == ob_value)
                if r:
                    if obj in result:
                        continue
                    else:
                        result.append(obj)
                else:
                    continue

        return result

    def __init__(self, *args, **kw):

        # Make sure the cache is initialized.
        self.__initialize_cache()

        # For now, lets make this simple and treat fields with no special
        # syntax (underlines, mainly) as our schema.
        self._special_fields = ["_timestamp", "_uuid"]
        self._fields = []
        for field in dir(self):
            if field.startswith("_"):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, field)) in [types.FunctionType,
                                              types.MethodType]:
                continue
            self._fields.append(field)

        if kw.get("timestamp", False):
            self._timestamp = int(time.time())
            self.timestamp = property(
                fget = lambda: self._timestamp,
                fset = lambda v: None,
                fdel = None,
                doc = "Object creation timestamp")

        if kw.get("uuid", False):
            self._uuid = str(uuid.uuid4())
            self.uuid = property(
                fget = lambda: self._uuid,
                fset = lambda v: None,
                fdel = None,
                doc = "Object UUID")

        self.__cache.append(self)

    def uncache(self):
        """ Removes the object from the state cache forcibly.
        """

        self.__cache.remove(self)

    def as_dict(self):
        """ Returns the dictionary representation of the fields
            in this object.
        """

        obj = {}

        for val in self._fields + self._special_fields:
            if not hasattr(self, val):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, val)) in [types.FunctionType,
                                            types.MethodType]:
                continue
            obj.update({val: getattr(self, val)})

        return obj

    def to_json(self):
        """ Converts the object into JSON form.
            Simple, right?
        """

        return json.dumps(self.as_dict())

    def from_json(self, data):
        """ Converts the JSON data back into an object, then loads
            the data into the model instance.
        """

        obj = json.loads(data)

        if not isinstance(obj, dict):
            raise TypeError("Expected JSON serialized dictionary, not %s" % (
                type(obj)))

        for k, v in obj.iteritems():
            # We need to make sure the data is sanitized a little bit.
            if k.startswith("_") and k not in self._special_fields:
                continue
            if k in self._fields:
                setattr(self, k, v)


class CachingBrineState(BrineState):
    """ The caching brine state works a lot like a regular brine state,
        except that the caching version will maintain a list of "dirty"
        attributes. This is useful in the case that you are trying to
        keep your state / models updated and consistent with some sort
        of upstream datastore.
    """

    def __init__(self, *args, **kw):

        BrineState.__init__(self, *args, **kw)

        # The "dirty" cache list is just a list of fields that have been
        # updated.
        self.__dirty = []

        # After initializing the regular brine state stuff, take the field
        # list and overwrite the values with getters and setters for tracking
        # dirty state.
#        pdb.set_trace()
        for field in self._fields:
            field_initial = getattr(self, field, None)
            field_prop = property(
                fget = lambda: getattr(self, "_" + field, None),
                fset = lambda v: self.__update_field(field, v),
                fdel = None)
            setattr(self, field, field_prop)

    def __update_field(self, field, value):
        """ Does the simple update and dirty marking of the field.
        """

        if field not in self.__dirty:
            self.__dirty.append(field)

        setattr(self, "_" + field, value)

    def as_dict(self):
        """ Returns the dictionary representation of the fields
            in this object.
        """

        obj = {}

        for val in self._fields + self._special_fields:
            if not hasattr(self, "_" + val):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, "_" + val)) in [types.FunctionType,
                                                  types.MethodType]:
                continue
            obj.update({val: getattr(self, "_" + val)})

        return obj
    
    def unmark(self, *fields):
        """ Unmarks some field as dirty. Should only be called after
            the upstream is updated or only if you know what you're doing!
        """

        for field in fields:
            if field not in self.__dirty:
                continue

            self.__dirty.remove(field)

    def dirty_dict(self):
        """ Dumps a dictionary of dirty fields.
        """

        obj = {}
        for val in self.__dirty:
            if not hasattr(self, val):
                continue
            # Also, make sure this isn't a function.
            if type(getattr(self, val)) in [types.FunctionType,
                                            types.MethodType]:
                continue
            obj.update({val: getattr(self, val)})

        return obj

    def dirty_json(self):
        """ Dumps the dirty dictionary as JSON.
        """

        return json.dumps(self.dirty_dict())


