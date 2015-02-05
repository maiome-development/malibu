#!/usr/bin/env python2.7

class DBResultList(list):

    def __init__(self, extend = None):

        if isinstance(extend, list):
            for item in extend:
                if isinstance(item, DBMapper):
                    self.append(item)
                else: continue

    def filter_equals(self, key, val):
        """ filter_equals(key, val) ->
              filters database find result based on
              key-value equality.
        """

        res = DBResultList()

        for dbo in self:
            try:
                if getattr(dbo, "_%s" % (key)) == val:
                    res.append(dbo)
                else: continue
            except: continue

        return res

    def filter_iequals(self, key, val):
        """ filter_iequals(key, val) ->
              filters database find result based on
              case insensitive key-value equality.
              assumes that db attribute and val are strings.
        """

        res = DBResultList()

        for dbo in self:
            try:
                if getattr(dbo, "_%s" % (key)).lower() == val.lower():
                    res.append(dbo)
                else: continue
            except: continue

        return res

    def filter_inequals(self, key, val):
        """ filter_inequals(key, val) ->
              filters database find result based on
              key-value inequality.
        """

        res = DBResultList()

        for dbo in self:
            try:
                if getattr(dbo, "_%s" % (key)) != val:
                    res.append(dbo)
                else: continue
            except: continue

        return res

    def filter_regex(self, key, regex):
        """ filter_regex(key, regex) ->
              filters database find result based on
              regex value matching.
        """

        res = DBResultList()

        for dbo in self:
            try:
                if re.match(regex, getattr(dbo, "_%s" % (key))) != None:
                    res.append(dbo)
                else: continue
            except: continue

        return res

