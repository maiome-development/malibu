#!/usr/bin/env python

import copy, urllib2, json
from urllib2 import urlopen

""" We need to write some better documentation for this crap.
    Either that, or we just need to re-write the configuration stuff
    from scratch and actually document it this time.
"""

class ConfigurationSection(dict):
    """ modified dictionary that returns none for invalid keys
    """
    
    def __init__(self):

        dict.__init__(self)
        
        self.mutable = True
    
    def __getitem__(self, key):
    
        try: return dict.__getitem__(self, key)
        except (IndexError, KeyError) as e:
            raise KeyError("Unknown configuration key '%s'." % (key))
    
    def __setitem__(self, key, value):
    
        if self.mutable:
            self.update({ key: value })
        else:
            raise AttributeError("This section is not mutable.")
    
    def set_mutable(self, mutable):
    
        self.mutable = mutable
    
    def set(self, key, value):
    
        return self.__setitem__(key, value)
    
    def get(self, key):
    
        return self.__getitem__(key)
    
    def get_list(self, key, delimiter = ",", default = []):
    
        try:
            val = self.get(key)
            return val.split(delimiter) if len(val) > 0 else default
        except: return default

    def get_string(self, key, default = ""):
    
        try:
            if str(self.get(key)) == '!None': return None
            return str(self.get(key)) or default
        except: raise
    
    def get_int(self, key, default = None):
    
        try: return int(self.get(key)) or default
        except: return default
    
    def get_bool(self, key, default = False):
    
        try:
            val = self.get(key) or default
            if isinstance(val, bool):
                return val
            elif isinstance(val, str):
                if val.lower() == 'true':
                    self.set(key, True)
                    return True
                elif val.lower() == 'false':
                    self.set(key, False)
                    return False
                else:
                    return default
            elif isinstanct(val, int):
                if val == 1:
                    self.set(key, True)
                    return True
                elif val == 0:
                    self.set(key, False)
                    return False
                else:
                    return default
            else:
                return default
        except: return default

class SectionPromise(object):
    """ this is a configuration section promise
        to make resolution of linked sections post-load
        easier.
    """
    
    promises = []
    
    def __init__(self, config, section, key, link):
        
        self.config = config
        self.section = section
        self.key = key
        self.link = link
        SectionPromise.promises.append(self)

    def resolve(self):
    
        section = self.config.get_section(self.section)
        link = self.onfig.get_section(self.link)
        target = section.get(self.key)

        if isinstance(target, list):
            target.remove(self)
            target.append(link)
            section.set(self.key, target)
        else:
            section.set(self.key, link)

class Configuration(object):
    """ 
        This definitely needs to be documented.
    """

    def __init__(self):
        """ initialise the container
            store in key:value format withing the certain category
        """

        self.__container = ConfigurationSection()
        self.loaded = False
        
    def __add_section(self, section_name):
        """ adds a new configuration section to the main dictionary.
        """
        
        section = ConfigurationSection()
        self.__container.set(section_name, section)
        
        return section
    
    def __remove_section(self, section_name):
        """ removes a section from the main dictionary.
        """
        
        del self.__container[section_name]

    def __resolve_links(self):
        """ resolves all linked references.
        """
        
        for promise in SectionPromise.promises:
            promise.resolve()
        
        SectionPromise.promises = []

    def has_section(self, section_name):
        """ return if x has a section
        """

        return section_name in self.__container

    def get_section(self, section_name):
        """ return a raw/direct reference to a section
        """

        return self.__container[section_name] if self.__container.__contains__(section_name) else None
    
    def unload(self):
        """ unload an entire configuration
        """

        self.__container.clear()
        self.loaded = False
    
    def reload(self):
        """ reload the configuration from the initially specified file
        """

        self.unload()
        self.load(self._filename)
    
    def load(self, filename):
        """
            load(filename)
            
            filename -> name of the file to load.
        """

        try:
            fobj = open(filename, 'r')
            self._filename = filename
            self.load_file(fobj)
        except:
            raise InputError("Invalid filename '%s'." % (filename))

    def load_file(self, fobj):
        """ load a file and read in the categories and variables
        """

        if self.loaded: self.__container.clear()
        section_name = None

        for line in f.readlines():
            line = line.strip('\n').lstrip()
        
            if line.startswith('#') or line.startswith('//') or line.startswith(';'):
                continue
            elif line.startswith('[') and line.endswith(']'):
                # This is the beginning of a section tag.
                section_name = line[1:-1]
                if not self.get_section(section_name):
                    self.__add_section(section_name)
                continue
            elif '=' in line:
                set = line.split('=')
                l = len(set[0])
                # strip whitespace
                set[0] = set[0].strip()
                set[1] = set[1].lstrip() if set[1] is not '' or ' ' else None
                
                if set[1][-1] == ';': set[1] = set[1][0:-1]
                section = self.get_section(section_name)
                
                if set[1].startswith('+'): # typed reference / variable
                    decl = set[1].split(':')
                    datatype = decl[0][1:]
                    value = decl[1]
                    
                    if datatype.lower() == 'file':
                        try:
                            section.set(set[0], open(value, 'r'))
                        except:
                            try: section.set(set[0], open(value, 'w+'))
                            except: section.set(set[0], None)
                    elif datatype.lower() == 'url':
                        try: section.set(set[0], urlopen(value))
                        except: section.set(set[0], None)
                    elif datatype.lower() == 'list':
                        try: listdata = json.loads('%s' % (value))
                        except: listdata = []
                        repl = []
                        for item in listdata:
                            if item.startswith('@'):
                                link_name = item[1:]
                                if not self.get_section(link_name):
                                    repl.append(SectionPromise(self, section_name, set[0], link_name))
                                else:
                                    link = self.get_section(link_name)
                                    repl.append(link)
                            else: repl.append(item)
                        section.set(set[0], repl)
                elif set[1].startswith('@'): # linked reference / section reference
                    link_name = set[1][1:]
                    if not self.get_section(link_name):
                        section.set(set[0], SectionPromise(self, section_name, set[0], link_name))
                    else:
                        link = self.get_section(link_name)
                        section.set(set[0], link)
                else: section.set(set[0], set[1])
                continue
            else:
                continue
        self.__resolve_links()
        self.loaded = True
        f.close()
