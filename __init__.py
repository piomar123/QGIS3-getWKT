# -*- coding: utf-8 -*-
"""
/***************************************************************************
 getwkt3
                                 A QGIS plugin
 This plugin displays the selected features' WKT representation.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-03-13
        copyright            : (C) 2018 by Paul Skeen
        email                : paulskeen@spatialecology.com.au
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load getwkt3 class from file getwkt3.
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .getwkt3 import getwkt3
    return getwkt3(iface)
