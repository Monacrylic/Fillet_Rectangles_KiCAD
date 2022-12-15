# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class RadiusInputDialog
###########################################################################

class RadiusInputDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 428,93 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( 428,93 ), wx.Size( -1,-1 ) )

		fgSizer1 = wx.FlexGridSizer( 3, 3, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )

		self.tx1 = wx.StaticText( self, wx.ID_ANY, u"Enter fillet radius(mm): ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tx1.Wrap( -1 )

		fgSizer1.Add( self.tx1, 0, wx.ALL, 5 )

		self.t1 = wx.TextCtrl( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.t1, 0, wx.ALL, 5 )

		self.b1 = wx.Button( self, wx.ID_ANY, u"run", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.b1, 0, wx.ALL, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.b1.Bind( wx.EVT_BUTTON, self.runScript )
		self.t1.Bind( wx.EVT_TEXT_ENTER, self.runScript )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def runScript( self, event ):
		event.Skip()
