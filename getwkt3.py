# -*- coding: utf-8 -*-
"""
/***************************************************************************
 getwkt3
                                 A QGIS plugin
 This plugin displays the selected features' WKT representation.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-03-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Paul Skeen
        email                : paulskeen@spatialecology.com.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .getwkt3_dialog import getwkt3Dialog

class getwkt3:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'getwkt3_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        # Create the dialog (after translation) and keep reference
        self.dlg = getwkt3Dialog()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Get WKT')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'getwkt3')
        self.toolbar.setObjectName(u'getwkt3')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('getwkt3', message)


    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/getwkt3/wkt.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Get WKT String'),
            callback=self.run_wkt,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/getwkt3/ewkt.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Get EWKT String'),
            callback=self.run_ewkt,
            parent=self.iface.mainWindow())

        icon_path = ':/plugins/getwkt3/json.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Get JSON String'),
            callback=self.run_json,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Get WKT'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run_wkt(self):
        """Runs tool to extract WKT"""
        self.run('wkt')

    def run_ewkt(self):
        """Runs tool to extract EWKT"""
        self.run('ewkt')

    def run_json(self):
        """Runs tool to extract JSON"""
        self.run('json')

    def run(self, out_type):
        """Run method that performs all the real work"""
        mc = self.iface.mapCanvas()
        layer = mc.currentLayer()
        if layer is None:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> No selected layer')
        elif layer.type() != QgsMapLayerType(0):
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> Layer selected is not vector')
        elif layer.selectedFeatureCount() == 0:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> No feature selected')
        elif layer.selectedFeatureCount() > 1:
            self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
            'ERROR:</strong> More than one feature is selected')
        else:
            feat = layer.selectedFeatures()
            if feat is None:
                self.dlg.wktTextEdit.setHtml('<strong style="color:red">'\
                'ERROR:</strong> No selected features')
            else:
                if out_type == 'wkt':
                    text = feat[0].geometry().asWkt()
                elif out_type == 'ewkt':
                    try:
                        authid = layer.crs().authid()
                        auth, srid = authid.split(':')
                        if auth != 'EPSG':
                            srid = -1
                    except Exception:
                        srid = -1
                    wkt = feat[0].geometry().asWkt()
                    text = 'SRID={0};{1}'.format(srid, wkt)
                elif out_type == 'json':
                    text = feat[0].geometry().asJson()
                else:
                    text = '[{0}] Not Implemented'.format(out_type)
                self.dlg.wktTextEdit.setText("{0}".format(text))
        self.dlg.show()
        # Run the dialog event loop
        self.dlg.exec_()
