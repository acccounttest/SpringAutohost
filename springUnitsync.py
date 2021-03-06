# -*- coding: ISO-8859-1 -*-
import unitsync
import springCompile


class SpringUnitsync:
	def __init__ (self, ClassServer):
		self.Server = ClassServer
		self.Debug = ClassServer.Debug
		self.SpringCompile = None
		self.Maps = {}
		self.Mods = {}
		self.LogicTest = self.Server.LogicTest
		self.Load ()
	
	
	def Load (self, Version = '', ReCompile = 0):
		self.Debug ('INFO', str (Version))
		if not Version and self.Server.Config['General'].has_key ('SpringBuildDefault'):
			Version = self.Server.Config['General']['SpringBuildDefault']
		
		if Version:
			if not self.SpringCompile:
				self.SpringCompile = springCompile.SpringCompile (self.Server)
			Result = self.SpringCompile.GetSpringVersion (Version, ReCompile)
			if Result and type (Result) is dict and Result.has_key ('Path'):
				self.Unitsync = unitsync.Unitsync (Result['Path'] + '/libunitsync.so')
			else:
				self.Debug ('ERROR', 'BUILD FAILED')
				return (None)
		else:
			Version = 'Default'
			self.Unitsync = unitsync.Unitsync (self.Server.Config['General']['PathUnitsync'])
		
		self.Unitsync.UnInit ()
		self.Unitsync.Init (True, 1)
			
		if not self.LogicTest:
			self.LoadMaps (Version)
		self.LoadMods (Version)
		return (True)


	def LoadMaps (self, Version):
		self.Debug ('INFO', Version)
		self.Maps[Version] = {}
		for iMap in range (0, self.Unitsync.GetMapCount ()):
			Map = self.Unitsync.GetMapName (iMap)
			self.Debug ('INFO', 'Load map::' + str (Map))
			self.Maps[Version][Map] = {
				'Hash':self.SignInt (self.Unitsync.GetMapChecksum (iMap)),
				'X':self.Unitsync.GetMapWidth (iMap),
				'Y':self.Unitsync.GetMapHeight (iMap),
				'Description':self.Unitsync.GetMapDescription (iMap),
			}
			if self.Unitsync.GetMapPosCount (iMap):
				self.Maps[Version][Map]['StartPos'] = {}
				for iPos in range (0, self.Unitsync.GetMapPosCount (iMap)):
					self.Maps[Version][Map]['StartPos'][iPos] = {
						'X':self.Unitsync.GetMapPosX (iMap, iPos),
						'Y':self.Unitsync.GetMapPosZ (iMap, iPos),
					}
			if self.Unitsync.GetMapOptionCount (Map):
				self.Maps[Version][Map]['Options'] = {}
				for iOpt in range (0, self.Unitsync.GetMapOptionCount (Map)):
					Option = self.LoadOption (iOpt)
					if len (Option) > 0:
						self.Maps[Version][Map]['Options'][Option['Key']] = Option
	
		
	def LoadMods (self, Version):
		self.Debug ('INFO', Version)
		self.Mods[Version] = {}
		for iMod in range (0, self.Unitsync.GetPrimaryModCount ()):
			self.Unitsync.RemoveAllArchives ()
			self.Unitsync.AddAllArchives (self.Unitsync.GetPrimaryModArchive (iMod))
			Mod = self.Unitsync.GetPrimaryModName (iMod)
			self.Debug ('INFO', 'Load mod::' + str (Mod))
			self.Mods[Version][Mod] = {
				'Hash':self.SignInt (self.Unitsync.GetPrimaryModChecksum (iMod)),
				'Title':self.Unitsync.GetPrimaryModName (iMod),
				'Sides':{},
				'Options':{},
				'AI':{},
				'Units':{},
			}
			if self.Unitsync.GetSideCount():
				for iSide in xrange (self.Unitsync.GetSideCount()):
					self.Mods[Version][Mod]['Sides'][iSide] = self.Unitsync.GetSideName (iSide)
			if self.Unitsync.GetModOptionCount ():
				for iOpt in xrange (self.Unitsync.GetModOptionCount ()):
					Option = self.LoadOption (iOpt)
					if len (Option) > 0:
						self.Mods[Version][Mod]['Options'][Option['Key']] = Option
			if self.Unitsync.GetSkirmishAICount ():
				for iAI in range (0, self.Unitsync.GetSkirmishAICount ()):
					self.Mods[Version][Mod]['AI'][iAI] = {}
					for iAII in range (0, self.Unitsync.GetSkirmishAIInfoCount (iAI)):
						self.Mods[Version][Mod]['AI'][iAI][self.Unitsync.GetInfoKey (iAII)] = self.Unitsync.GetInfoValue (iAII)
			self.Unitsync.ProcessUnits ()
			if self.Unitsync.GetUnitCount ():
				for iUnit in range (0, self.Unitsync.GetUnitCount ()):
					self.Mods[Version][Mod]['Units'][self.Unitsync.GetUnitName (iUnit)] = self.Unitsync.GetFullUnitName (iUnit)
	
	
	def LoadOption (self, iOpt):
		Data = {}
		if self.Unitsync.GetOptionType (iOpt) == 1:
			Data = {
				'Key':self.Unitsync.GetOptionKey (iOpt),
				'Title':self.Unitsync.GetOptionName (iOpt),
				'Type':'Boolean',
				'Default':self.Unitsync.GetOptionBoolDef (iOpt),
				'Description':self.Unitsync.GetOptionDesc (iOpt),
			}
		elif self.Unitsync.GetOptionType (iOpt) == 2:
			Data = {
				'Key':self.Unitsync.GetOptionKey (iOpt),
				'Title':self.Unitsync.GetOptionName (iOpt),
				'Type':'Select',
				'Default':self.Unitsync.GetOptionListDef (iOpt),
				'Description':self.Unitsync.GetOptionDesc (iOpt),
				'Options':{},
			}
			if self.Unitsync.GetOptionListCount (iOpt):
				for iItem in range (0, self.Unitsync.GetOptionListCount (iOpt)):
					Data['Options'][self.Unitsync.GetOptionListItemKey (iOpt, iItem)] = self.Unitsync.GetOptionListItemName (iOpt, iItem) + ' (' + self.Unitsync.GetOptionListItemDesc (iOpt, iItem) + ')'
		elif self.Unitsync.GetOptionType (iOpt) == 3:
			Data = {
				'Key':self.Unitsync.GetOptionKey (iOpt),
				'Title':self.Unitsync.GetOptionName (iOpt),
				'Type':'Numeric',
				'Default':self.ConvertFloat (self.Unitsync.GetOptionNumberDef (iOpt)),
				'Min':self.ConvertFloat (self.Unitsync.GetOptionNumberMin (iOpt)),
				'Max':self.ConvertFloat (self.Unitsync.GetOptionNumberMax (iOpt)),
				'Step':self.ConvertFloat (self.Unitsync.GetOptionNumberStep (iOpt)),
				'Description':self.Unitsync.GetOptionDesc (iOpt),
			}
		elif self.Unitsync.GetOptionType (iOpt) == 4:
			Data = {
				'Key':self.Unitsync.GetOptionKey (iOpt),
				'Title':self.Unitsync.GetOptionName (iOpt),
				'Type':'String',
				'Default':self.Unitsync.GetOptionStringDef (iOpt),
				'MaxLength':self.Unitsync.GetOptionStringMaxLen (iOpt),
				'Description':self.Unitsync.GetOptionDesc (iOpt),
			}
		elif self.Unitsync.GetOptionType (iOpt) == 5:
			Ignore = 1	# Group header
		else:
			self.Debug ('ERROR', 'Unkown options type (' + str (self.Unitsync.GetOptionType (iOpt)) + ')')
		return (Data)
	
	
	def SignInt (self, Int):
		if Int > 2147483648:
			Int = Int - 2147483648 * 2
		return (Int)
	
	
	def ConvertFloat (self, Value):
		if type (Value) is float:
			return (round (Value, 5))
		else:
			return (Value)