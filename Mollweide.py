"""
    A simple Mollweide Projection class
    With project function and some plotting function
    By Jie Zheng, 2016-07, at Tucson
"""

import numpy as np
import matplotlib.pyplot as plt


class moll :
    """ Do Mollweide projection
    """

    def __init__ (self, xsize=1.0, ysize=1.0,
                  lon_range=None, lat_range=(-90.0, 90.0),
                  lon_center=180.0, lon_rev=True, lat_mode=0) :
        """ Init the object
        all param unit is degree, or pixels
        param xsize: image coord size in x, half part, default 1.0
        param ysize: image coord size in y, half part, default 1.0
        param lon_range: 2-element tuple, range of longnitude (ra), default 0 to 360
        param lat_range: 2-element tuple, range of latitude (dec), default -90 to 90
        param lon_center: center longnitude, default 180
        param lon_rev: is longnitude reversed, from 360 to 0, default True for sky
        param lat_mode: 0 for stananrd mollweide project, 1 for line dec project
        """
        self.xsize = xsize
        self.ysize = ysize
        self.lon_center = lon_center
        self.lon_rev = lon_rev
        self.lat_mode = lat_mode

        if lon_range == None :
            lon_range = (lon_center - 180, lon_center + 180)

        if lon_rev ^ (lon_range[0] < lon_range[1]) :
            self.lon_range  = np.array(lon_range)
        else :
            self.lon_range  = np.array((lon_range[1], lon_range[0]))
        if lat_range[0] < lat_range[1] :
            self.lat_range  = np.array(lat_range)
        else :
            self.lat_range  = np.array((lat_range[1], lat_range[0]))

        #TODO: use theta & delta
        theta = self._theta(self.lat_range)
        delta = self._delta(self.lon_range)
        if delta[0] == delta[1] : delta = (-1, 1)

        if 0.0 > theta[0] and theta[1] > 0.0 :
            atheta = np.array([theta[0], theta[0], theta[1], theta[1],      0.0,      0.0])
            adelta = np.array([delta[0], delta[1], delta[0], delta[1], delta[0], delta[1]])
        else  :
            atheta = np.array([theta[0], theta[0], theta[1], theta[1]])
            adelta = np.array([delta[0], delta[1], delta[0], delta[1]])
        x = self._x(adelta, atheta)
        y = self._y(adelta, theta)
        self.x_range = (min(x), max(x))
        self.y_range = (y[0], y[1])

    def _inxy (self, x, y) :
        return self.x_range[0] <= x and x <= self.x_range[1] and \
               self.y_range[0] <= y and y <= self.y_range[1]

    def _in (self, lon, lat) :
        """ Tell if a point is inside lon/lat range
        param lon: longnitude of point, in degree
        param lat: latitide of point, in degree
        """
        x, y = self.project(lon, lat)
        return self._inxy(x, y)

    def _toarray(self, a) :
        """ Transfer scalar, list or tuple to numpy array
        """
        if isinstance(a, np.ndarray) :
            return a
        elif isinstance(a, list) or isinstance(a, tuple) :
            return np.array(a)
        else :
            return np.array((a,))

    def _delta(self, lon) :
        d = ((lon - self.lon_center) / 180.0 + 1.0) % 2.0 - 1.0 # make sure -1.0 ~ +1.0
        if self.lon_rev : d = -d
        return d

    def _theta(self, lat) :
        return lat / 180.0 * np.pi

    def _x (self, delta, theta) :
        """ Get x coord from delta and theta
        param delta: relative longnitude distance to center, in fraction
        param theta: relative latitide distance to center, in radias
        """
        return self.xsize * delta * np.cos(theta)

    def _y (self, delta, theta) :
        """ Get y coord from delta and theta
        param delta: relative longnitude distance to center, in fraction
        param theta: relative latitide distance to center, in radias
        """
        if self.lat_mode == 0 :
            return self.ysize * np.sin(theta)
        else :
            return self.ysize * theta / np.pi * 2.0

    def project (self, lon, lat) :
        """ Project lon/lat to x/y, the MOST IMPORTANT function
        param lon: longnitude of points, in degree
        param lat: latitide of points, in degree
        lon and lat can be scalar, list, tuple or ndarray
        must have same length, or scalar. Scalar will be broadcasted.
        """
        lon = self._toarray(lon)
        lat = self._toarray(lat)
        nlon, nlat = len(lon), len(lat)
        if nlon < nlat and nlon == 1 :
            lon = np.tile(lon, nlat)
        elif nlon > nlat and nlat == 1 :
            lat = np.tile(lat, nlon)
        elif nlon != nlat:
            raise IndexError

        theta = self._theta(lat)
        delta = self._delta(lon)
        x = self._x(delta, theta)
        y = self._y(delta, theta)
        return x, y

    def grid (self, lat_step = 15.0, lon_step = 30.0,
              lat_lab_lon = None, lon_lab_lat = None,
              colorstyle = "k:", lab_color = "k") :
        """ Draw lon/lat (ra/dec) grid
        param lat_step: step of latitude (dec) line, default 15
        param lon_step: step of longnitude (ra) line, default 30
        param lat_lab_lon: longnitude where latitude label print, if None, not print
        param lon_lab_lat: latitude where longnitude label print, if None, not print
        param colorstyle: color and style of grid line, default black dotted line
        param lab_color: color of lat/lon label, default black
        """
        delta = np.arange(-1, 1.1, 0.1)
        y0 = np.zeros_like(delta)
        for theta in np.arange(0.0, 1.6, lat_step / 180.0 * np.pi):
            x = self._x(delta, theta)
            y = y0 + self._y(delta, theta)
            plt.plot(x,  y, colorstyle)
            if theta > 0 : plt.plot(x, -y, colorstyle)

        theta = np.append(np.insert(np.arange(-1.5, 1.51, 0.1), 0, -1.57), 1.57)
        y = self._y(0, theta)
        for delta in np.arange(0.0, 1.0001, lon_step / 180.0) :
            x = self._x(delta, theta)
            plt.plot(x, y, colorstyle)
            if delta > 0 : plt.plot(-x, y, colorstyle)

        if lat_lab_lon != None :
            for lat in np.arange(0, 90.001, lat_step) :
                #x, y = self.project(lat_lab_lon, lat)
                #if self._in(lat_lab_lon, lat) :
                    #plt.text(x, y, "%5.1f"%(lat), color=lab_color)
                self.text(lat_lab_lon, lat, "%5.1f"%(lat), color=lab_color)
                if lat > 0.0 : #and self._in(lat_lab_lon, -lat) :
                    #plt.text(x, -y, "%5.1f"%(-lat), color=lab_color)
                    self.text(lat_lab_lon, -lat, "%5.1f"%(-lat), color=lab_color)

        if lon_lab_lat != None :
            for lon in np.arange(0, 180.001, lon_step) :
                #x, y = self.project(self.lon_center + lon, lon_lab_lat)
                #if self._in(self.lon_center + lon, lon_lab_lat) :
                    #plt.text(x, y, "%5.1f"%((self.lon_center + lon) % 360.0), color=lab_color)
                self.text(self.lon_center + lon, lon_lab_lat, "%5.1f"%((self.lon_center + lon) % 360.0), color=lab_color)
                if lon > 0.0 : #and self._in(self.lon_center - lon, lon_lab_lat) :
                    #plt.text(-x, y, "%5.1f"%((self.lon_center - lon) % 360.0), color=lab_color)
                    self.text(self.lon_center - lon, lon_lab_lat, "%5.1f"%((self.lon_center - lon) % 360.0), color=lab_color)

        plt.axis('off')
        plt.xlim(self.x_range)
        plt.ylim(self.y_range)

    def text (self, lon, lat, textstr, rangecheck=True, color="k") :
        x, y = self.project(lon, lat)
        if rangecheck and self._inxy(x, y) :
            plt.text(x, y, textstr, color=color)

    def annotate (self, textstr, lon, lat, textlon=None, textlat=None, arrowprops=dict(facecolor='black', shrink=0.05)) :
        x, y = self.project(lon, lat)
        if textlon != None and textlat != None :
            textx, texty = self.project(textlon, textlat)
            textxy = (textx, texty)
        else :
            textxy = None
        plt.annotate(textstr, xy=(x, y), textxy=textxy, arrowprops=arrowprops)

    def plotline (self, lon0, lon1, lat0, lat1, colorstyle=None, label=None, alpha=None, linewidth=None) :
        """ Plot a line from lon0/lat0 to lon1/lat1, by add interline point
        param lon0: longnitude of start point, in degree
        param lon1: longnitude of end point, in degree
        param lat0: latitide of start point, in degree
        param lat1: latitide of end point, in degree
        param colorstyle: color and style of line, default None
        """
        n = 10
        lon = np.linspace(lon0, lon1, n)
        lat = np.linspace(lat0, lat1, n)
        x, y = self.project(lon, lat)
        plt.plot(x, y, colorstyle, label=label, alpha=alpha, linewidth=linewidth)

    def polyline (self, lon, lat, colorstyle=None, close=False, label=None, alpha=None, linewidth=None) :
        """ Draw poly line to pass given point
        param lon: longnitude of points, in degree
        param lat: latitide of points, in degree
        param colorstyle: color and style of line, default None
        param close: if True, last point will connect to first
        """
        for p in range(1, len(lon)) :
            self.plotline(lon[p-1], lon[p], lat[p-1], lat[p], colorstyle,
                          label=label, alpha=alpha, linewidth=linewidth)
        if close :
            self.plotline(lon[-1], lon[0], lat[-1], lat[0], colorstyle,
                          label=label, alpha=alpha, linewidth=linewidth)

    def scatter (self, lon, lat, colorstyle=".", label=None, alpha=None) :
        """ Mark scatter point in map
        param lon: longnitude of points, in degree
        param lat: latitide of points, in degree
        """
        x, y = self.project(lon, lat)
        plt.plot(x, y, colorstyle, label=label, alpha=alpha)

    def plot (self, lon, lat, colorstyle=None, label=None, close=False) :
        """ plot line or scatter point in map
        param lon: longnitude of points, in degree
        param lat: latitide of points, in degree
        param colorstyle: color and style of line, default None
        param label: label of line or point
        param close: if True, last point will connect to first
        """
        # check scatter points or lines
        pass
