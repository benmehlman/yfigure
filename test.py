#!/usr/bin/env python
from yfigure import YAMLConfig

class MyConfig(YAMLConfig):
    config_files = [
        './test.yaml'
    ]

if __name__ == "__main__":

    print('\nTest with default configuration, set to "english" in the yaml file, would otherwise default to "root".')
    config = MyConfig()
    print('configuration=%s.' % config.configuration)
    print('hellotext=%s.' % config.hellotext)

    print('\nTest with configuration explicitly set to "spanish" in constructor, overrides any configuration selection in yaml.')
    config = MyConfig(configuration='spanish')
    print('configuration=%s.' % config.configuration)
    print('hellotext=%s.' % config.hellotext)
    
    