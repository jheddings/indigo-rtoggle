#!/usr/bin/env python2.5

import random

################################################################################
class Plugin(indigo.PluginBase):

    #---------------------------------------------------------------------------
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        self._initializeLogging(pluginPrefs)

    #---------------------------------------------------------------------------
    def __del__(self):
        indigo.PluginBase.__del__(self)

    #---------------------------------------------------------------------------
    def validatePrefsConfigUi(self, values):
        errors = indigo.Dict()

        devices = values.get('devices', '')

        return ((len(errors) == 0), values, errors)

    #---------------------------------------------------------------------------
    def closedPrefsConfigUi(self, values, canceled):
        if canceled: return

        self._initializeLogging(values)

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

        # XXX how to update the global dependencies with selected items?

        return ((len(errors) == 0), values, errors)

    #---------------------------------------------------------------------------
    def rtoggle(self, action):
        deviceList = action.props.get('deviceList', '')
        self.logger.debug('%d devices in list', len(deviceList))

        deviceId = int(random.choice(deviceList))

        if deviceId in indigo.devices:
            self.logger.debug('selected device: %d', deviceId)
            indigo.device.toggle(deviceId)
        else:
            self.logger.error('Invalid device in toggle group: %d', deviceId)

    #---------------------------------------------------------------------------
    def deviceListGenerator(self, filter='', valuesDict=None, typeId='', targetId=0):
        self.logger.debug('build device list')

        returnList = list()

        # only add devices that have an onState - e.g. can be turned on/off
        for devId in indigo.devices.iterkeys():
            device = indigo.devices.get(devId)
            if hasattr(device, 'onState'):
                returnList.append((devId, device.name))

        return returnList

    #---------------------------------------------------------------------------
    def _initializeLogging(self, values):
        levelTxt = values.get('logLevel', None)

        if levelTxt is None:
            self.logLevel = 20
        else:
            self.logLevel = int(levelTxt)

        self.indigo_log_handler.setLevel(self.logLevel)

