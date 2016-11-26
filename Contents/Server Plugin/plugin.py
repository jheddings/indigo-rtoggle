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

        # TODO update description

        return ((len(errors) == 0), values, errors)

    #---------------------------------------------------------------------------
    def rtoggle(self, action):
        self.debugLog('rtoggle()')

        deviceList = action.props.get('deviceList', '')
        self.debugLog('%s devices in list' % len(deviceList))

        deviceId = random.choice(deviceList)
        self.debugLog('selected device: %s' % deviceId)

        # TODO error handling

        indigo.device.toggle(deviceId)

    #---------------------------------------------------------------------------
    def deviceListGenerator(self, filter='', valuesDict=None, typeId='', targetId=0):
        self.debugLog('deviceListGenerator(filter=%s, typeId=%s, targetId=%s)' % (filter, typeId, str(targetId)))

        returnList = list()
        deviceList = valuesDict.get("memberDevices", "").split(",")

        for devId in indigo.devices.iterkeys():
            # don't allow the current device
            # TODO only allow devices that support toggle
            if str(devId) not in deviceList:
                device = indigo.devices.get(devId)
                returnList.append((devId, device.name))

        return returnList

