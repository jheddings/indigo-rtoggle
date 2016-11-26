#!/usr/bin/env python2.5

import random

################################################################################
class Plugin(indigo.PluginBase):

    #---------------------------------------------------------------------------
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get('debug', False)

    #---------------------------------------------------------------------------
    def __del__(self):
        indigo.PluginBase.__del__(self)

    #---------------------------------------------------------------------------
    def toggleDebugging(self):
        self.debug = not self.debug
        self.pluginPrefs['debug'] = self.debug

    #---------------------------------------------------------------------------
    def validatePrefsConfigUi(self, values):
        errors = indigo.Dict()

        devices = values.get('devices', '')

        return ((len(errors) == 0), values, errors)

    #---------------------------------------------------------------------------
    def closedPrefsConfigUi(self, values, canceled):
        if (not canceled):
            self.debug = values.get('debug', False)

    #---------------------------------------------------------------------------
    def validateActionConfigUi(self, values, typeId, devId):
        errors = indigo.Dict()

        deviceList = values.get('deviceList', list())
        numDevices = len(deviceList)

        if (numDevices < 1):
            errors['deviceList'] = 'must select at least one device'
        elif (numDevices > 1):
            values['description'] = 'toggle group - %s devices' % numDevices
        else:
            values['description'] = 'toggle group - 1 device'

        return ((len(errors) == 0), values, errors)

    #---------------------------------------------------------------------------
    def rtoggle(self, action):
        self.debugLog('rtoggle()')

        deviceList = action.props.get('deviceList', '')
        self.debugLog('%s devices in list' % len(deviceList))

        deviceId = int(random.choice(deviceList))
        self.debugLog('selected device: %s' % deviceId)

        # TODO error handling

        indigo.device.toggle(deviceId)

    #---------------------------------------------------------------------------
    def deviceListGenerator(self, filter='', valuesDict=None, typeId='', targetId=0):
        self.debugLog('deviceListGenerator(filter=%s, typeId=%s, targetId=%s)' % (filter, typeId, str(targetId)))

        returnList = list()

        # only add devices that have an onState - e.g. can be turned on/off
        for devId in indigo.devices.iterkeys():
            device = indigo.devices.get(devId)
            if hasattr(device, 'onState'):
                returnList.append((devId, device.name))

        return returnList

