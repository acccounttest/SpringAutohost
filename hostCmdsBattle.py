# -*- coding: ISO-8859-1 -*-
import hostCmdsBattleLogic
import hostCmdsBattleBalance

class HostCmdsBattle:
	def __init__ (self, ClassHostCmds, ClassServer, ClassHost):
		self.Server = ClassServer
		self.Debug = ClassServer.Debug
		self.Debug ('INFO', 'HostCmdsBattle Init')
		self.Host = ClassHost
		self.HostCmds = ClassHostCmds
		self.Logic = hostCmdsBattleLogic.HostCmdsBattleLogic (self, ClassServer, ClassHost)
		self.Balance = hostCmdsBattleBalance.HostCmdsBattleBalance (self, ClassServer, ClassHost)
		self.Commands = {	# 0 = Field, 1 = Return to where (Source, PM, Battle, if List = [True return, False return]), 2 = Ussage example, 3 = Usage desc, 4 = Category (if available), 5 = Extended help (if available)
			'map':[['*'], 'BattleMe', '!map <map name>', 'Changes the map to <map name>'],
			'maps':[['O*'], 'PM', '!maps <optional search>', 'Return a list with all the available maps'],
			'mods':[['O*'], 'PM', '!mods <optional search>', 'Return a list with all the available mods'],
			'start':[[], 'BattleMe', '!start', 'Starts the battle if possible'],
			'stop':[[], 'BattleMe', '!stop', 'Stops the battle'],
			'lock':[['OB'], 'BattleMe', '!lock [0/1]', 'Locks/unlocks the battle'],
			'kick':[['V'], 'BattleMe', '!kick <user>', 'Kicks <user> from the battle'],
			'ring':[['OV'], 'BattleMe', '!ring [<user>]', 'Rings a specific user or all unready users'],
			'addbox':[['I', 'I', 'I', 'I', 'OI'], 'Source', '!addbox <Left 0-100> <Top 0-100> <Right 0-100> <Bottom 0-100> <Team 1-16>', 'Adds a startbox (if no team is specified, the next empty one is used)'],
			'udp':[['*'], 'Source', '!udp <command>', 'Sends a command to the spring server'],
			'forcestart':[[], 'BattleMe', '!forcestart', 'Force start the battle'],
			'info':[[], 'PM', '!info', 'Returns the status of the current battle'],
			'addbot':[['I', 'I', 'V', 'V6', '*'], 'BattleMe', '!addbot 1 1 CORE FFFFFF E323AI', 'Add a bot to the battle (Team, Ally, Side, Hex RGB Color, Bot)'],
			'spec':[['V'], 'BattleMe', '!spec <User>', 'Spectates the specified user'],
			'fixid':[[], 'BattleMe', '!fixid', 'Fix the player IDs'],
			'balance':[[], 'BattleMe', '!balance', 'Balances the battle users based on rank'],
			'openbattle':[[], 'Source', '!openbattle', 'Opens a battle'],
			'spring':[['V'], 'Source', '!spring <spring version>', 'Sets the spring version to the specified tag'],
			'modoption':[['V', 'O*'], ['BattleMeRequester', 'PM'], '!modoption <option> <value>', 'Sets a mod option'],
			'startpos':[['I'], 'Source', '!startpos <0-3>', 'Sets the start pos (0 Fixed, 1 Randon, 2 Choose in-game, 3 Choose now)'],
			'hcp':[['V', 'I'], 'Source', '!hcp <user> <hcp>', 'Sets the handicap for the specified user'],
			'mod':[['*'], 'Source', '!mod <mod>', 'Rehosts with the specified mod'],
			'saveboxes':[[], 'Source', '!saveboxes', 'Saves the current box setup'],
			'kickbots':[[], 'Source', '!kickbots', 'Kicks all bots from the battle'],
			'preset':[['V'], 'Source', '!preset <preset name>', 'Loads the specified preset settings'],
			'savepreset':[['V'], 'Source', '!savepreset <preset name>', 'Saves the current battle settings with the <preset name>'],
			'teams':[['OI'], 'Source', '!teams <>|<1-16>', 'Sets or displays the number of teams in the battle'],
			'mapoption':[['V', 'O*'], ['BattleMeRequester', 'PM'], '!mapoption <option> <value>', 'Sets a map option'],
			'disableunit':[['V'], 'Source', '!disableunit <unit>', 'Disbles a unit'],
			'enableunitsall':[[], 'Source', '!enableunitsall', 'Enables all units'],
			'id':[['V', 'I'], 'BattleMe', '!id <user> <new id>', 'Changes a users ID'],
			'team':[['V', 'I'], 'BattleMe', '!team <user> <new id>', 'Changes a users team'],
			'color':[['V', 'V'], 'BattleMe', '!color <user> <Hex color>', 'Changes a users color'],
			'split':[['V', 'I', 'OB'], 'BattleMe', '!split <type> <size> <optional 1 to clear boxes>', 'Creates multiple boxes'],
			'clearbox':[['I'], 'BattleMe', '!clearbox <0 = all|1-16>', 'Removes one or all boxes'],
			'fixcolor':[['V'], 'BattleMe', '!fixcolor <user>', 'Fixes the <user>s battle color'],
			'fixcolors':[[], 'BattleMe', '!fixcolors', 'Fixes all users battle colors'],
			'botside':[['V', 'V'], 'BattleMe', '!botside <bot> <side>', 'Forces <bot> to switch side to <side>'],
			'nextmap':[[], 'BattleMe', '!nextmap', 'Switches to the next map in the list'],
			'prevmap':[[], 'BattleMe', '!prevmap', 'Switches to the prev map in the list'],
			'randommap':[[], 'BattleMe', '!randommap', 'Switches to a random map in the list (does not work with prev/next map)'],
			'reordermaps':[[], 'BattleMe', '!reordermaps', 'Reorders the map list'],
		}
		for Command in self.Commands:
			self.HostCmds.Commands[Command] = self.Commands[Command]
		

	def HandleInput (self, Command, Data):
		self.Debug ('DEBUG', 'HandleInput::' + str (Command) + '::' + str (Data))
		
		if Command == 'map':
			return (self.Logic.LogicChangeMap (Data[0]))
		elif Command == 'maps':
			if len (Data) == 1:
				return (self.Logic.LogicListMaps (Data[0]))
			else:
				return (self.Logic.LogicListMaps ())
		elif Command == 'mods':
			if len (Data) == 1:
				return (self.Logic.LogicListMods (Data[0]))
			else:
				return (self.Logic.LogicListMods ())
		elif Command == 'start':
			return (self.Logic.LogicStartBattle ())
		elif Command == 'stop':
			Return = self.Host.Spring.SpringStop ()
			return ([True, Return])
		elif Command == 'lock':
			if len (Data) == 1:
				Lock = Data[0]
			else:
				Lock = {0:1, 1:0}[self.Host.Lobby.Battles[self.Host.Lobby.BattleID]['Locked']]
			self.Host.Lobby.BattleLock (Lock)
			if Lock:
				return ([True, 'Battle locked'])
			else:
				return ([True, 'Battle unlocked'])
		elif Command == 'kick':
			return (self.Logic.LogicKick (Data[0]))
		elif Command == 'ring':
			if len (Data) == 1:
				return (self.Logic.LogicRing (Data[0]))
			else:
				return (self.Logic.LogicRing ())
		elif Command == 'addbox':
			if len (Data) == 4:
				return (self.Logic.LogicAddBox (Data[0], Data[1], Data[2], Data[3]))
			else:
				return (self.Logic.LogicAddBox (Data[0], Data[1], Data[2], Data[3], Data[4]))
		elif Command == 'udp':
			self.Host.Spring.SpringTalk (Data[0])
		elif Command == 'forcestart':
			self.Host.Spring.SpringTalk ('/forcestart')
			return ('Battle started')
		elif Command == 'info':
			return (self.Logic.LogicInfo ())
		elif Command == 'addbot':
			return (self.Logic.LogicAddBot (Data[0], Data[1], Data[2], Data[3], Data[4]))
		elif Command == 'spec':
			return (self.Logic.LogicSpec (Data[0]))
		elif Command == 'fixid':
			return (self.Logic.LogicFixID ())
		elif Command == 'balance':
			return (self.Balance.LogicBalance ())
		elif Command == 'openbattle':
			return (self.Logic.LogicOpenBattle ())
		elif Command == 'spring':
			return (self.Logic.LogicSetSpringVersion (Data[0]))
		elif Command == 'modoption':
			if len (Data) == 2:
				return (self.Logic.LogicSetModOption (Data[0], Data[1]))
			else:
				return (self.Logic.LogicSetModOption (Data[0]))
		elif Command == 'startpos':
			return (self.Logic.LogicSetStartPos (Data[0]))
		elif Command == 'hcp':
			return (self.Logic.LogicSetHandicap (Data[0], Data[1]))
		elif Command == 'mod':
			return (self.Logic.LogicReHostWithMod (Data[0]))
		elif Command == 'saveboxes':
			return (self.Logic.LogicSaveBoxes ())
		elif Command == 'kickbots':
			return (self.Logic.LogicKickBots ())
		elif Command == 'preset':
			return (self.Logic.LogicLoadPreset (Data[0]))
		elif Command == 'savepreset':
			return (self.Logic.LogicSavePreset (Data[0]))
		elif Command == 'teams':
			if len (Data) == 1:
				return (self.Logic.LogicSetTeams (Data[0]))
			else:
				return ([True, 'No. of teams: ' + str (self.Host.Battle['Teams'])])
		elif Command == 'mapoption':
			if len (Data) == 2:
				return (self.Logic.LogicSetMapOption (Data[0], Data[1]))
			else:
				return (self.Logic.LogicSetMapOption (Data[0]))
		elif Command == 'disableunit':
			return (self.Logic.LogicDisableUnit (Data[0]))
		elif Command == 'enableunitsall':
			return (self.Logic.LogicEnableUnitsAll ())
		elif Command == 'id':
			return (self.Logic.LogicForceID (Data[0], Data[1]))
		elif Command == 'team':
			return (self.Logic.LogicForceTeam (Data[0], Data[1]))
		elif Command == 'color':
			return (self.Logic.LogicForceColor (Data[0], Data[1]))
		elif Command == 'split':
			if len (Data) == 3:
				return (self.Logic.LogicSplitBox (Data[0], Data[1], Data[2]))
			else:
				return (self.Logic.LogicSplitBox (Data[0], Data[1]))
		elif Command == 'clearbox':
			return (self.Logic.LogicClearBox (Data[0]))
		elif Command == 'fixcolor':
			return (self.Logic.LogicFixColors (Data[0]))
		elif Command == 'fixcolors':
			return (self.Logic.LogicFixColors ())
		elif Command == 'botside':
			return (self.Logic.LogicSetBotSide (Data[0], Data[1]))
		elif Command == 'nextmap':
			return (self.Logic.LogicChangeMap (None, 'Next'))
		elif Command == 'prevmap':
			return (self.Logic.LogicChangeMap (None, 'Prev'))
		elif Command == 'randommap':
			return (self.Logic.LogicChangeMap (None, 'Random'))
		elif Command == 'reordermaps':
			return (self.Logic.LogicChangeMap (None, 'Reorder'))
