'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
 Default values for the new configuration.
   
 (c) 2011 by flonatel GmhH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.Constraints import Constraints

# pylint: disable=R0903
class DefaultValues:
    '''This calls all the appropriate functions to set the 
       default values.
       Instead of merging in here everything, the information
       is placed where it should be.'''

    def __init__(self):
        '''Hidden constructor for utility class.'''
        assert(False)

    @staticmethod
    def set_default_values(cfg):
        '''Calls the appropriate functions to set the default
           configuration values.'''
        Constraints.set_default_values(cfg)
