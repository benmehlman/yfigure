
import os
from os.path import expanduser
import sys
import yaml

"""
A SIMPLE BUT EFFECTIVE CONFIGURATION CLASS FOR PYTHON

# import YAMLConfig from wherever it is..
from .yfigure import YAMLConfig

# subclass YAMLConfig to make config class for your application, list config_files in the order you want them tried.
class MyConfig(YAMLConfig):
    config_files = (
       '~/myapp.conf',
       '/etc/myapp.conf'
    )
    
# THERE ARE A FEW TRICKS FOR READING THE CONF AND SELECTING DIFFERENT CONFIGURATIONS FROM THE SAME FILE.
# First, by default, if you do a simple:
    
config = MyConfig()
 
# ..and you put your configuration values in the file.. then they will be read and the top level yaml elements will
# become attributes of config, so you can do:
# IN YAML:
hellotext: hello
goodbyetext: goodbye
    
# then get the value of hellotext:
print(config.hellotext)

# but you can also have multiple configurations within the same file:
# IN YAML:
    
english:
    hellotext: hello
    goodbyetext: goodbye

spanish:
    hellotext: hola
    goodbyetext: adios

# Then you can select them one of two ways, either from your code or from within yaml.
# Within YAML, there's a special config top level variable called "configuration":
    
configuration: spanish
     
# Now everything under spanish becomes the top level of the config and everything else in the file is ignored.
    
# You can also select it from within your code by passing it to the constructor of the config class:
config = MyConfig(configuration='spanish')
    
# You can force the base (non-nested) configuration by passing configuration='root' anywhere you can specify a configuration name.

# If you wanted to control it from an environment variable you could:
import os # import os if you haven't already...
config = MyConfig(configuration=os.environ['MYAPP_CONFIG'])

# You have a choice there.. the way I read the environment variable, it'll raise an exception if MYAPP_CONFIG isn't set.
# but let's say you do:
config = MyConfig(configuration=os.environ.get('MYAPP_CONFIG'))

# in that case if MYAPP_CONFIG is not set, it'll pass configuration=None, which defaults to root.
# If the value of configuration (other than None or 'root') is not present in the top level of the YAML, ValueError is raised.

# Anything YAML supports is ok, any level of nesting, but only the first level is put in attributes, so if you do, in YAML:
db:
    name: thegoods
    servers: 
        - godfather1
        - godfather2
    
# You would access the top level as a direct member of config but everything else is just as you would expect:
config.db['name']
config.db['servers'][0]

# There's no easy way to override actual config values from the environment, only which section of the config file is used.
# But it would be easy enough to add.
 
"""

def open_config(pathnames, verbose=False):

    def log(s):
        if verbose:
            sys.stderr.write(s)

    pathname = stream = None
    for option in pathnames:
        if pathname:
            log(',')

        pathname = expanduser(option)
        log(' %s' % pathname)

        if not os.path.isfile(pathname):
            log(" NO")
            continue

        try:
            stream = open(pathname)
            log(" YES")
            break
        except Exception as e:
            log("\n%s: %s.\n" % (pathname, e))
            raise

    log(".\n")
    if stream:
        return stream
    raise FileNotFoundError('None of: %s were found.' % str(pathnames))

class YAMLConfig(object):

    def __init__(self, config_files=None, configuration=None, verbose=False):
        config_files = getattr(self, 'config_files', config_files)
        error_tpl = type(self).__name__ + ' Error loading file: %s.'

        if not config_files:
            raise NotImplementedError(
                'YAMLConfig requires "config_files" as either a member of a subclass, or a kwarg of  __init__.  It was neither.'
            )

        try:
            with open_config(config_files) as stream:
                self._data = data = yaml.load(stream, Loader=yaml.FullLoader)

                if configuration == '_default_':
                    configuration = None
                self.configuration = configuration or data.get('configuration', 'root')

                if isinstance(data, dict):
                    if not self.configuration == 'root':
                        if not self.configuration in data:
                            raise ValueError(error_tpl % ('configuration named "%s" not found in YAML.' % self.configuration))
                        data = data[self.configuration]

                    for a, v in data.items():
                       setattr(self, a, v)

        except Exception as e:
            sys.stderr.write((error_tpl % e) + '\n')
            if isinstance(e, FileNotFoundError):
                raise
            raise ValueError(error_tpl % e)


