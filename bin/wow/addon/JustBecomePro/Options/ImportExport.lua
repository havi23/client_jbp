-- --------------------
-- JustBecomePro
-- Originally by Nephthys of Hyjal <lieandswell@yahoo.com>

-- Other contributions by:
--		Sweetmms of Blackrock, Oozebull of Twisting Nether, Oodyboo of Mug'thol,
--		Banjankri of Blackrock, Predeter of Proudmoore, Xenyr of Aszune

-- Currently maintained by
-- Cybeloras of Aerie Peak
-- --------------------


if not JBP then return end

local JBP = JBP
local L = JBP.L
local print = JBP.print

-- GLOBALS: JUSTBECOMEPRO_VERSIONNUMBER

local get = JBP.get

local tonumber, tostring, type, pairs, ipairs, tinsert, tremove, sort, wipe, next, rawget =
	  tonumber, tostring, type, pairs, ipairs, tinsert, tremove, sort, wipe, next, rawget
local strfind, strmatch, format, gsub, strsub, strtrim, max, min, strlower, floor, log10 =
	  strfind, strmatch, format, gsub, strsub, strtrim, max, min, strlower, floor, log10



local function showGUIDConflictHelp(editbox, ...)
	if not JBP.HELP:IsCodeRegistered("IMPORT_NEWGUIDS") then
		JBP.HELP:NewCode("IMPORT_NEWGUIDS", 1, false)
	end
	JBP.HELP:Show{
		code = "IMPORT_NEWGUIDS",
		icon = nil,
		relativeTo = editbox,
		x = 0,
		y = 0,
		text = format(...)
	}
end

JBP:RegisterCallback("JBP_OPTIONS_LOADED", function()
	JBP.HELP:NewCode("ICON_EXPORT_MULTIPLE", 10, false)
	JBP.HELP:NewCode("ICON_EXPORT_DOCOPY", 11, true)
end)





local SharableDataType

local EDITBOX




local Item = JBP:NewClass("SettingsItem")
Item:MakeInstancesWeak()

function Item:OnNewInstance(type, parent)
	assert(type)

	self.Type = type
	self.extra = {}
	
	if parent then
		self:SetParent(parent)
	end
end

function Item:GetEditBox()
	return EDITBOX
end

function Item:SetExtra(k, v)
	self.extra[k] = v
end
function Item:GetExtra(k)
	return self.extra[k]
end

function Item:SetParent(parent)
	self.parent = parent
	self.Version = self.Version or parent.Version
	self.ImportSource = self.ImportSource or parent.ImportSource
end


function Item:CreateMenuEntry(doLabel)
	local info = JBP.DD:CreateInfo()
	info.value = self
	info.hasArrow = true
	info.notCheckable = true

	SharableDataType.types[self.Type]:Import_CreateMenuEntry(info, self, doLabel)

	if doLabel then
		-- Color everything before the first colon a light blue (highlights the type of data being exported, for clarity)
		info.text = info.text:gsub("^(.-):", "|cff00ffff%1|r:")
	end

	if self:GetExtra("SourcePlayer") then
		local fromLine = FROM .. " " .. self:GetExtra("SourcePlayer")

		if info.tooltipText then
			info.tooltipText = info.tooltipText .. "\r\n\r\n" .. fromLine
		else
			if not info.tooltipTitle then
				info.tooltipTitle = fromLine
			else
				info.tooltipText = fromLine
			end
		end

	end

	self.Header = info.text

	JBP.DD:AddButton(info)
end

function Item:BuildChildMenu()
	if self.Header then
		local info = JBP.DD:CreateInfo()
		info.text = self.Header
		info.isTitle = true
		info.notCheckable = true
		JBP.DD:AddButton(info)

		JBP.DD:AddSpacer()
	end

	SharableDataType.types[self.Type]:RunMenuBuilders(self)
end

function Item:Import(...)
	self:AssertSelfIsInstance()
	
	local results = JBP:DetectImportedLua(self.Settings)
	local source = self.ImportSource.type

	if source == "Profile" or source == "Backup" or not results then
		JBP:Import(self, ...)
	else
		JBP:ImportPendingConfirmation(self, results, {JBP.Import, JBP, self, ...})
	end
end







local Bundle = JBP:NewClass("SettingsBundle")
Bundle:MakeInstancesWeak()
function Bundle:OnNewInstance(type)
	assert(type)

	self.Type = type
	self.Items = {}
end

function Bundle:Add(Item)
	assert(Item.class == JBP.Classes.SettingsItem)
	assert(Item.Type == self.Type)

	tinsert(self.Items, Item)
end
function Bundle:InItems()
	return pairs(self.Items)
end
function Bundle:GetLength()
	return #self.Items
end

function Bundle:First()
	return self.Items[1]
end
function Bundle:Last()
	return self.Items[#self.Items]
end

function Bundle:Evaluate()
	local numPerGroup = SharableDataType.types[self.Type].numPerGroup

	-- Not needed now that we have scrollable dropdowns.
	--[[if #self.Items > numPerGroup then
		local Bundle = Bundle:New(self.Type)

		for n, Item in self:InItems() do
			if Bundle:GetLength() >= numPerGroup then
				Bundle:CreateGroupedMenuEntry()
				Bundle = Bundle:New(self.Type)
			end

			Bundle:Add(Item)
		end
		Bundle:CreateGroupedMenuEntry()
	else]]

	if self.Header then
		local info = JBP.DD:CreateInfo()
		info.text = self.Header
		info.isTitle = true
		info.notCheckable = true
		JBP.DD:AddButton(info)

		JBP.DD:AddSpacer()
	end

	for n, Item in self:InItems() do
		Item:CreateMenuEntry()
	end

	--end
end

--[[
function Bundle:CreateGroupedMenuEntry()
	local info = JBP.DD:CreateInfo()
	info.notCheckable = true
	info.hasArrow = true
	info.value = self

	info.text = SharableDataType.types[self.Type]:Import_GetGroupedBundleEntryText(self)
	self.Header = info.text

	JBP.DD:AddButton(info)
end]]

function Bundle:CreateParentedMenuEntry(text)
	if self:GetLength() > 0 then
		local info = JBP.DD:CreateInfo()
		info.text = text
		self.Header = text
		info.notCheckable = true
		info.hasArrow = true
		info.value = self
		JBP.DD:AddButton(info)

		return true
	end
end




-- -----------------------
-- DATA TYPES
-- -----------------------

SharableDataType = JBP:NewClass("SharableDataType")
SharableDataType.types = {}
SharableDataType.numPerGroup = 15
SharableDataType.extrasMap = {}

function SharableDataType:OnNewInstance(type, order)
	JBP:ValidateType("2 (type)", "SharableDataType:New(type, order)", type, "string")
	JBP:ValidateType("3 (order)", "SharableDataType:New(type, order)", order, "number")
	
	self.type = type
	self.order = order
	SharableDataType.types[type] = self
	self.MenuBuilders = {}
end
function SharableDataType:RegisterMenuBuilder(order, func)
	tinsert(self.MenuBuilders, {
		order = order,
		func = func,
	})
	
	JBP:SortOrderedTables(self.MenuBuilders)
end
function SharableDataType:RunMenuBuilders(Item)
	for i, data in ipairs(self.MenuBuilders) do
		JBP.safecall(data.func, Item)
	end
end
function SharableDataType:AddExtras(Item, ...)
	for i, v in pairs(self.extrasMap) do
		Item:SetExtra(v, select(i, ...))
	end
end








---------- Database ----------
local database = SharableDataType:New("database", 40)








---------- Profile ----------
local profile = SharableDataType:New("profile", 30)
profile.extrasMap = {"Name"}

function profile:Import_ImportData(Item, profileName)
	if profileName then

		-- generate a new name if the profile already exists
		while JBP.db.profiles[profileName] do
			profileName = JBP.oneUpString(profileName)
		end

		-- put the data in the profile (no reason to CTIPWM when we can just do this) and set the profile
		JBP.db.profiles[profileName] = CopyTable(Item.Settings)
		JBP.db:SetProfile(profileName)
	else
		JBP.db:ResetProfile()
		JBP:CopyTableInPlaceUsingDestinationMeta(Item.Settings, JBP.db.profile, true)
	end

	if Item.Version then
		if Item.Version > JUSTBECOMEPRO_VERSIONNUMBER then
			JBP:Print(L["FROMNEWERVERSION"])
		else
			JBP:UpgradeProfile()
		end
	end
end

function profile:Import_CreateMenuEntry(info, Item, doLabel)
	info.text = Item:GetExtra("Name")

	if doLabel then
		info.text = L["fPROFILE"]:format(info.text or "<UNNAMED>")
	end
end

function profile:Import_GetGroupedBundleEntryText(Bundle)
	local First = Bundle:First():GetExtra("Name")
	local Last = Bundle:Last():GetExtra("Name")

	return L["UIPANEL_PROFILES"] .. ": " ..
	(First:match("(.-)%-") or First:gsub(1, 20)):trim(" -") .. " - " ..
	(Last:match("(.-)%-") or Last:gsub(1, 20)):trim(" -")
end


-- Current Profile
database:RegisterMenuBuilder(10, function(Item_database)
	local db = Item_database.Settings
	local currentProfile = JBP.db:GetCurrentProfile()
	
	-- This might not evaluate to true if the import source is the backup database
	-- and this profile didn't exist when backup was created
	if db.profiles[currentProfile] then
		local Item = Item:New("profile")

		Item:SetParent(Item_database)
		Item.Settings = db.profiles[currentProfile]
		Item:SetExtra("Name", currentProfile)

		Item:CreateMenuEntry()

		JBP.DD:AddSpacer()
	end
end)

-- All other profiles
database:RegisterMenuBuilder(20, function(Item_database)
	local db = Item_database.Settings
	local currentProfile = JBP.db:GetCurrentProfile()

	local Bundle = Bundle:New("profile")

	--other profiles
	for profilename, profiletable in JBP:OrderedPairs(db.profiles) do
		-- current profile and default are handled separately
		if profilename ~= currentProfile --[[and profilename ~= "Default"]] then
			local Item = Item:New("profile")

			Item:SetParent(Item_database)
			Item.Settings = profiletable
			Item.Version = profiletable.Version
			Item:SetExtra("Name", profilename)

			Bundle:Add(Item)
		end
	end

	JBP.DD:AddSpacer()
	
	Bundle:Evaluate()
end)

-- Default Profile
--[[database:RegisterMenuBuilder(30, function(Item_database)
	local db = Item_database.Settings
	local currentProfile = JBP.db:GetCurrentProfile()
	
	--default profile
	if db.profiles["Default"] and currentProfile ~= "Default" then
		local Item = Item:New("profile")

		Item:SetParent(Item_database)
		Item.Settings = db.profiles.Default
		Item.Version = db.profiles.Default.Version
		Item:SetExtra("Name", "Default")

		Item:CreateMenuEntry()
	end
end)]]


-- Copy Profile
profile:RegisterMenuBuilder(10, function(Item_profile)
	-- copy entire profile - overwrite current
	local info = JBP.DD:CreateInfo()
	info.text = L["IMPORT_PROFILE"] .. " - " .. L["IMPORT_PROFILE_OVERWRITE"]:format(JBP.db:GetCurrentProfile())
	info.func = function()
		Item_profile:Import()
	end
	info.notCheckable = true
	JBP.DD:AddButton(info)

	-- copy entire profile - create new profile
	local info = JBP.DD:CreateInfo()
	info.text = L["IMPORT_PROFILE"] .. " - " .. L["IMPORT_PROFILE_NEW"]
	info.func = function()
		Item_profile:Import(Item_profile:GetExtra("Name"))
	end
	info.notCheckable = true
	JBP.DD:AddButton(info)

	JBP.DD:AddSpacer()
end)



function profile:Export_SetButtonAttributes(editbox, info)
	local text = L["fPROFILE"]:format(JBP.db:GetCurrentProfile())
	info.text = text
	info.tooltipTitle = text
end
function profile:Export_GetArgs(editbox)
	-- settings, defaults, ...
	return JBP.db.profile, JBP.Defaults.profile, JBP.db:GetCurrentProfile()
end






---------- Gloabl Groups ----------
local globalgroups = SharableDataType:New("globalgroups", 20)

function globalgroups:Export_SetButtonAttributes(editbox, info)
	local text = L["fGROUPS"]:format(L["EXPORT_ALLGLOBALGROUPS"])
	info.text = text
	info.tooltipTitle = text
	info.func = function(button, ExportDestination)
		-- type, settings, defaults, ...
		self.doHideWarning = true

		ExportDestination:Export(self.type, {}, {})

		if self.doHideWarning then
			JBP.HELP:Hide("ICON_EXPORT_MULTIPLE")
		end
	end
end
JBP:RegisterCallback("JBP_EXPORT_SETTINGS_REQUESTED", function(event, strings, type, settings)
	if type == "globalgroups" then
		tremove(strings, 1)
		local num = 0
		for gs, domain, groupID in JBP:InGroupSettings() do
			if domain == "global" then
				num = num + 1
				JBP:GetSettingsStrings(strings, "group", gs, JBP.Group_Defaults, groupID)
			end
		end

		if num ~= #strings then
			globalgroups.doHideWarning = false
		end
	end
end)








---------- Group ----------
local group = SharableDataType:New("group", 10)
group.numPerGroup = 10
group.extrasMap = {"groupID"}
group.spaceAfter = true

local function remapGUIDs(data, GUIDmap)
	for k, v in pairs(data) do
		local type = type(v)
		if type == "table" then
			remapGUIDs(v, GUIDmap)
		elseif type == "string" then
			if GUIDmap[v] then
				data[k] = GUIDmap[v]
			else
				for oldGUID, newGUID in pairs(GUIDmap) do
					oldGUID = oldGUID:gsub("([%-%+])", "%%%1")
					if v:find(oldGUID) then
						data[k] = v:gsub(oldGUID, newGUID)
					end
				end
			end
		end
	end
end

function group:Import_ImportData(Item_group, domain, createNewGroup, oldgroupID, destgroup)
	print(domain, createNewGroup, oldgroupID, destgroup)
	local group
	if createNewGroup then
		group = JBP:Group_Add(domain, nil)
	else
		group = destgroup
	end

	local version = Item_group.Version

	JBP.db[domain].Groups[group.ID] = nil -- restore defaults, table recreated when passed in to CTIPWM
	local gs = group:GetSettings()
	JBP:CopyTableInPlaceUsingDestinationMeta(Item_group.Settings, gs, true)

	if version < 70000 then
		gs.__UPGRADEHELPER_OLDGROUPID = oldgroupID
	elseif version >= 70000	then
		local existingGUIDs = {}

		local GUIDmap = {}

		for gs2 in JBP:InGroupSettings() do
			if gs ~= gs2 then
				existingGUIDs[gs2.GUID] = true
			end
		end
		for ics, gs2 in JBP:InIconSettings() do
			if ics.GUID and ics.GUID ~= "" then
				if gs ~= gs2 then
					existingGUIDs[ics.GUID] = true
				else
					GUIDmap[ics.GUID] = JBP:GenerateGUID("icon", JBP.CONST.GUID_SIZE)
				end
			end
		end

		GUIDmap[gs.GUID] = JBP:GenerateGUID("group", JBP.CONST.GUID_SIZE)

		for k, v in pairs(GUIDmap) do
			if not existingGUIDs[k] then
				GUIDmap[k] = nil
			end
		end

		if next(GUIDmap) then
			local groupCount, iconCount = 0, 0
			for k, v in pairs(GUIDmap) do
				local dataType = JBP:ParseGUID(k)
				if dataType == "group" then
					groupCount = groupCount + 1
				elseif dataType == "icon" then
					iconCount = iconCount + 1
				end
			end

			JBP:Printf(L["IMPORT_NEWGUIDS"], groupCount, iconCount)
			showGUIDConflictHelp(EDITBOX, L["IMPORT_NEWGUIDS"], groupCount, iconCount)

			remapGUIDs(gs, GUIDmap)
		end
	end

	if version then
		if version > JUSTBECOMEPRO_VERSIONNUMBER then
			JBP:Print(L["FROMNEWERVERSION"])
		else
			JBP:StartUpgrade("group", version, gs, domain, group.ID)
		end
	end

	group:Setup()
	if group:IsVisible() then
		JustBecomePro_GroupImportFlash:Play(group)

	elseif not JBP.Locked then
		JBP:Printf(L["IMPORT_GROUPNOVISIBLE"])
	end
end

function group:Import_CreateMenuEntry(info, Item, doLabel)
	local gs = Item.Settings
	local groupID = Item:GetExtra("groupID")

	info.text = JBP:GetGroupName(gs.Name, groupID)
	info.tooltipTitle = format(L["fGROUP"], groupID)
	info.tooltipText = 	(L["UIPANEL_ROWS"] .. ": " .. (gs.Rows or 1) .. "\r\n") ..
					L["UIPANEL_COLUMNS"] .. ": " .. (gs.Columns or 4) ..
					((gs.Enabled ~= false and "") or "\r\n(" .. L["DISABLED"] .. ")")

	if doLabel then
		info.text = L["fGROUP"]:format(info.text)
	end
end

function group:Import_GetGroupedBundleEntryText(Bundle)
	return L["UIPANEL_GROUPS"] .. ": " ..
	Bundle:First():GetExtra("groupID") .. " - " ..
	Bundle:Last():GetExtra("groupID")
end


-- Global Group Listing
database:RegisterMenuBuilder(15, function(Item_database)
	
	local global = Item_database.Settings.global
	local Bundle = Bundle:New("group")

	local numGroups = global.NumGroups

	if numGroups and numGroups > 1 then
		for groupID, gs in JBP:OrderedPairs(global.Groups) do
			if groupID >= 1 and groupID <= numGroups then
				local Item = Item:New("group")

				Item:SetParent(Item_database)
				Item.Settings = gs
				Item:SetExtra("groupID", groupID)

				Bundle:Add(Item)
				
			end
		end

		Bundle:CreateParentedMenuEntry(L["UIPANEL_GROUPS_GLOBAL"])
	end
end)

-- Profile Group Listing
profile:RegisterMenuBuilder(40, function(Item_profile)
	-- group header
	local info = JBP.DD:CreateInfo()
	info.text = L["UIPANEL_GROUPS"]
	info.isTitle = true
	info.notCheckable = true
	JBP.DD:AddButton(info)


	local profile = Item_profile.Settings
	local Bundle = Bundle:New("group")

	local numGroups = tonumber(profile.NumGroups) or 1

	if profile.Groups then
		for groupID, gs in JBP:OrderedPairs(profile.Groups) do
			if groupID >= 1 and groupID <= numGroups then
				local Item = Item:New("group")

				Item:SetParent(Item_profile)
				Item.Settings = gs
				Item:SetExtra("groupID", groupID)

				Bundle:Add(Item)
			end
		end
	end

	Bundle:Evaluate()
end)


-- Copy Group
group:RegisterMenuBuilder(20, function(Item_group)
	local groupID = Item_group:GetExtra("groupID")
	local gs = Item_group.Settings

	local IMPORTS, EXPORTS = EDITBOX:GetAvailableImportExportTypes()

	local group = IMPORTS.group_overwrite

	-- copy entire group - overwrite current
	local info = JBP.DD:CreateInfo()
	-- IMPORT_PROFILE_OVERWRITE is used here even though we aren't importing a profile
	info.text = L["COPYGROUP"] .. " - " .. L["IMPORT_PROFILE_OVERWRITE"]:format(group and group:GetGroupName() or "?")
	info.func = function()
		Item_group:Import(group.Domain, false, groupID, group)
	end
	info.notCheckable = true
	info.disabled = not IMPORTS.group_overwrite
	JBP.DD:AddButton(info)

	-- copy entire group - create new group in profile
	local info = JBP.DD:CreateInfo()
	info.text = L["COPYGROUP"] .. " - " .. L["MAKENEWGROUP_PROFILE"]
	info.func = function()
		Item_group:Import("profile", true, groupID)
	end
	info.notCheckable = true
	JBP.DD:AddButton(info)

	-- copy entire group - create new group in global
	local info = JBP.DD:CreateInfo()
	info.text = L["COPYGROUP"] .. " - " .. L["MAKENEWGROUP_GLOBAL"]
	info.func = function()
		Item_group:Import("global", true, groupID)
	end
	info.notCheckable = true
	JBP.DD:AddButton(info)
end)




function group:Export_SetButtonAttributes(editbox, info)
	local IMPORTS, EXPORTS = editbox:GetAvailableImportExportTypes()
	local group = EXPORTS[self.type]
	
	local text = L["fGROUP"]:format(group:GetGroupName())
	info.text = text
	info.tooltipTitle = text
end

function group:Export_GetArgs(editbox)
	-- settings, defaults, ...
	local IMPORTS, EXPORTS = editbox:GetAvailableImportExportTypes()
	local group = EXPORTS[self.type]
	
	return group:GetSettings(), JBP.Group_Defaults, group.ID
end








---------- Icon ----------
local icon = SharableDataType:New("icon", 1)
icon.extrasMap = {}

function icon:Import_ImportData(Item)
	local IMPORTS, EXPORTS = EDITBOX:GetAvailableImportExportTypes()
	
	local icon = IMPORTS.icon
	local group = IMPORTS.group_overwrite
	local gs = group:GetSettings()

	gs.Icons[icon.ID] = nil -- restore defaults
	local ics = icon:GetSettings()
	JBP:CopyTableInPlaceUsingDestinationMeta(Item.Settings, ics, true)


	local version = Item.Version
	if version >= 70000 and ics.GUID ~= "" then
		local existed = false

		for ics2 in JBP:InIconSettings() do
			if ics2 ~= ics and ics2.GUID == ics.GUID then
				existed = true
				break
			end
		end

		if existed then
			JBP:Printf(L["IMPORT_NEWGUIDS"], 0, 1)
			showGUIDConflictHelp(EDITBOX, L["IMPORT_NEWGUIDS"], 0, 1)

			local GUIDmap = {
				[ics.GUID] = JBP:GenerateGUID("icon", JBP.CONST.GUID_SIZE)
			}
			remapGUIDs(ics, GUIDmap)
		end
	end


	if version then
		if version > JUSTBECOMEPRO_VERSIONNUMBER then
			JBP:Print(L["FROMNEWERVERSION"])
		else
			JBP:StartUpgrade("icon", version, ics, gs, icon.ID)
		end
	end
end

function icon:Import_CreateMenuEntry(info, Item, doLabel)
	local ics = Item.Settings
	local iconID = Item:GetExtra("iconID")

	local Item_group = Item.parent
	local groupID = Item_group and Item_group:GetExtra("groupID")
	local gs = Item_group and Item_group.Settings
	local version = Item.Version


	local IMPORTS, EXPORTS = EDITBOX:GetAvailableImportExportTypes()
	
	local text, textshort, tooltipText = JBP:GetIconMenuText(ics)
	if text:sub(-2) == "))" and iconID then
		textshort = textshort .. " " .. L["fICON"]:format(iconID)
	end
	info.text = textshort
	info.tooltipTitle = (groupID and format(L["GROUPICON"], JBP:GetGroupName(gs and gs.Name, groupID, 1), iconID)) or (iconID and L["fICON"]:format(iconID)) or L["ICON"]
		
	info.disabled = not IMPORTS.icon
	if info.disabled then
		info.tooltipText = L["IMPORT_ICON_DISABLED_DESC"]
		info.tooltipWhileDisabled = true
	else
		info.tooltipText = tooltipText
	end

	info.hasArrow = false

	info.icon = JBP:GuessIconTexture(ics)
	info.tCoordLeft = 0.07
	info.tCoordRight = 0.93
	info.tCoordTop = 0.07
	info.tCoordBottom = 0.93

	info.func = function()
		if ic and ic:IsVisible() then
			JBP.HELP:Show{
				code = "ICON_IMPORT_CURRENTPROFILE",
				icon = nil,
				relativeTo = EDITBOX,
				x = 0,
				y = 0,
				text = format(L["HELP_IMPORT_CURRENTPROFILE"])
			}
			IMPORTS.icon:SetInfo("texture", tex)
		else
			IMPORTS.icon:SetInfo("texture", nil)
		end
		
		if gs then
			JBP:PrepareIconSettingsForCopying(ics, gs)
		end
		
		Item:Import()
	end

	if doLabel then
		info.text = L["fICON"]:format(info.text)
	end
end

function icon:Import_GetGroupedBundleEntryText(Bundle)
	return L["UIPANEL_ICONS"] .. ": " ..
	Bundle:First():GetExtra("iconID") .. " - " ..
	Bundle:Last():GetExtra("iconID")
end


-- Group's Icons
group:RegisterMenuBuilder(30, function(Item_group)
	
	if Item_group.Settings.Icons then
		JBP.DD:AddSpacer()

		-- Header
		local info = JBP.DD:CreateInfo()
		info.text = L["UIPANEL_ICONS"]
		info.isTitle = true
		info.notCheckable = true
		JBP.DD:AddButton(info)


		local Bundle = Bundle:New("icon")

		for iconID, ics in JBP:OrderedPairs(Item_group.Settings.Icons) do
			if not JBP:DeepCompare(JBP.DEFAULT_ICON_SETTINGS, ics) then
				local Item = Item:New("icon")

				Item:SetParent(Item_group)
				Item.Settings = ics
				Item:SetExtra("iconID", iconID)

				Bundle:Add(Item)
			end
		end

		Bundle:Evaluate()
	end
end)


icon:RegisterMenuBuilder(10, function(Item_icon)
	Item_icon:CreateMenuEntry()
end)



function icon:Export_SetButtonAttributes(editbox, info)
	local IMPORTS, EXPORTS = editbox:GetAvailableImportExportTypes()
	local icon = EXPORTS.icon
	
	local text = L["fICON"]:format(JBP.get(icon.typeData.name))
	info.text = text
	info.tooltipTitle = text

	info.icon = icon.attributes.texture
	info.tCoordLeft = 0.07
	info.tCoordRight = 0.93
	info.tCoordTop = 0.07
	info.tCoordBottom = 0.93
end

function icon:Export_GetArgs(editbox)
	-- settings, defaults, ...
	local IMPORTS, EXPORTS = editbox:GetAvailableImportExportTypes()
	local icon = EXPORTS.icon
	
	local gs = icon.group:GetSettings()
	local ics = icon:GetSettings()
	JBP:PrepareIconSettingsForCopying(ics, gs)
	
	return ics, JBP.Icon_Defaults
end







-- -----------------------
-- IMPORT SOURCES
-- -----------------------

local ImportSource = JBP:NewClass("ImportSource")
ImportSource.types = {}

function ImportSource:OnNewInstance(type)
	self.type = type
	ImportSource.types[type] = self
end




---------- Profile ----------
local Profile = ImportSource:New("Profile")
Profile.displayText = L["IMPORT_FROMLOCAL"]

function Profile:HandleTopLevelMenu()
	local Item = Item:New("database")
	Item.ImportSource = self

	Item.Settings = JBP.db
	Item.Version = JustBecomeProDB.Version

	Item:BuildChildMenu()
end




---------- Backup ----------
local Backup = ImportSource:New("Backup")
Backup.displayText = L["IMPORT_FROMBACKUP"]
Backup.displayDescription = L["IMPORT_FROMBACKUP_DESC"]:format(JBP.BackupDate or "<backup disabled>")
Backup.displayDisabled = function()
	return not JBP.Backupdb
end

function Backup:HandleTopLevelMenu()
	if not JBP.Backupdb then return end
	local Item = Item:New("database")
	Item.ImportSource = self

	Item.Settings = JBP.Backupdb
	Item.Version = JBP.Backupdb.Version

	Item:BuildChildMenu()
end

function Backup:JBP_CONFIG_IMPORTEXPORT_DROPDOWNDRAW(event, destination)
	if destination == self then
		local info = JBP.DD:CreateInfo()
		info.text = "|cffff0000" .. L["IMPORT_FROMBACKUP_WARNING"]:format(JBP.BackupDate)
		info.isTitle = true
		info.notCheckable = true
		JBP.DD:AddButton(info)

		JBP.DD:AddSpacer()
	end
end

JBP:RegisterCallback("JBP_CONFIG_IMPORTEXPORT_DROPDOWNDRAW", Backup)




---------- String ----------
local String = ImportSource:New("String")
String.displayText = function()
	return (EDITBOX.DoPulseValidString and "|cff00ff00" or "") .. L["IMPORT_FROMSTRING"]
end
String.displayDisabled = function()
	local t = strtrim(EDITBOX:GetText())
	return not (t ~= "" and JBP:DeserializeData(t))
end
String.displayDescription = L["IMPORT_FROMSTRING_DESC"]

function String:HandleTopLevelMenu()
	local t = strtrim(EDITBOX:GetText())

	-- Unescape escaped pipes. Any pipes pasted into an editbox in wow will be escaped.
	t = t:gsub("||", "|")

	local editboxResults = t ~= "" and JBP:DeserializeData(t)

	if editboxResults then
		for _, result in pairs(editboxResults) do 
			local type = SharableDataType.types[result.type]

			local Item = Item:New(result.type)
			Item.ImportSource = self

			Item.Settings = result.data
			Item.Version = result.version
			type:AddExtras(Item, unpack(result))

			Item:CreateMenuEntry(true)
		end
	end
end




---------- Comm ----------
local Comm = ImportSource:New("Comm")
local DeserializedData = {}
Comm.displayText = L["IMPORT_FROMCOMM"]
Comm.displayDescription = L["IMPORT_FROMCOMM_DESC"]
Comm.displayDisabled = function()
	Comm:DeserializeReceivedData()
	return not (DeserializedData and next(DeserializedData))
end

function Comm:DeserializeReceivedData()
	if JBP.Received then
		 -- deserialize received comm
		for k, who in pairs(JBP.Received) do
			-- deserialize received data now because we dont do it as they are received; AceSerializer is only embedded in _Options
			if type(k) == "string" and who then
				local results = JBP:DeserializeData(k, true)
				if results then
					for _, result in pairs(results) do
						tinsert(DeserializedData, result)
						result.who = who
						JBP.Received[k] = nil
					end
				end
			end
		end
		if not next(JBP.Received) then
			JBP.Received = nil
		end
	end
end

function Comm:HandleTopLevelMenu(editbox)
	Comm:DeserializeReceivedData()
	
	for k, result in ipairs(DeserializedData) do
		local type = SharableDataType.types[result.type]

		local Item = Item:New(result.type)
		Item.ImportSource = self

		Item.Settings = result.data
		Item.Version = result.version
		Item:SetExtra("SourcePlayer", result.who)
		type:AddExtras(Item, unpack(result))

		Item:CreateMenuEntry(true)
	end
end








-- -----------------------
-- EXPORT DESTINATIONS
-- -----------------------


local ExportDestination = JBP:NewClass("ExportDestination")
ExportDestination.types = {}

function ExportDestination:OnNewInstance(type)
	self.type = type
	ExportDestination.types[type] = self
end

function ExportDestination:HandleTopLevelMenu()
	local IMPORTS, EXPORTS = EDITBOX:GetAvailableImportExportTypes()
	
	for k, dataType in JBP:OrderedPairs(SharableDataType.instances, JBP.OrderSort, true) do
		if EXPORTS[dataType.type] then
			local info = JBP.DD:CreateInfo()

			info.tooltipText = self.Export_DescriptionPrepend
			if dataType.Export_DescriptionAppend then
				info.tooltipText = info.tooltipText .. "\r\n\r\n" .. dataType.Export_DescriptionAppend
			end
			info.tooltipWhileDisabled = true
			info.notCheckable = true
			
			dataType:Export_SetButtonAttributes(EDITBOX, info)
			
			-- Color everything before the first colon a light blue (highlights the type of data being exported, for clarity)
			info.text = info.text:gsub("^(.-):", "|cff00ffff%1|r:")

			info.arg1 = self
			info.func = info.func or function(button, self)
				-- type, settings, defaults, ...
				self:Export(dataType.type, dataType:Export_GetArgs(EDITBOX))
			end
			
			JBP.DD:AddButton(info)

			if dataType.spaceAfter then
				JBP.DD:AddSpacer()
			end
		end
	end
end




---------- String ----------
local String = ExportDestination:New("String")
String.Export_DescriptionPrepend = L["EXPORT_TOSTRING_DESC"]

function String:Export(type, settings, defaults, ...)
	local strings = JBP:GetSettingsStrings(nil, type, settings, defaults, ...)

	local str = table.concat(strings, "\r\n\r\n")
		-- Escape any pipes so they can be copied correctly out of the textbox.
		:gsub("|", "||")

	str = JBP:MakeSerializedDataPretty(str)
	JBP.LastExportedString = str

	EDITBOX:SetText(str)
	EDITBOX:HighlightText()
	EDITBOX:SetFocus()

	JBP.DD:CloseDropDownMenus()

	JBP.HELP:Hide("ICON_EXPORT_MULTIPLE")
	if #strings > 1 then
		JBP.HELP:Show{
			code = "ICON_EXPORT_MULTIPLE",
			icon = nil,
			relativeTo = EDITBOX,
			x = 0,
			y = 0,
			text = format(L["HELP_EXPORT_MULTIPLE_STRING"])
		}
	end

	JBP.HELP:Show{
		code = "ICON_EXPORT_DOCOPY",
		icon = nil,
		relativeTo = EDITBOX,
		x = 0,
		y = 0,
		text = format(L["HELP_EXPORT_DOCOPY_" .. (IsMacClient() and "MAC" or "WIN")])
	}
end

function String:SetButtonAttributes(editbox, info)
	info.text = L["EXPORT_TOSTRING"]
	info.tooltipTitle = L["EXPORT_TOSTRING"]
	info.tooltipText = L["EXPORT_TOSTRING_DESC"]
	info.hasArrow = true
end




---------- Comm ----------
local Comm = ExportDestination:New("Comm")
Comm.Export_DescriptionPrepend = L["EXPORT_TOCOMM_DESC"]

function Comm:Export(type, settings, defaults, ...)
	local player = self.player
	if player and #player > 1 then
		local strings = JBP:GetSettingsStrings(nil, type, settings, defaults, ...)

		JBP.HELP:Hide("ICON_EXPORT_MULTIPLE")
		if #strings > 1 then
			JBP.HELP:Show{
				code = "ICON_EXPORT_MULTIPLE",
				icon = nil,
				relativeTo = EDITBOX,
				x = 0,
				y = 0,
				text = format(L["HELP_EXPORT_MULTIPLE_COMM"])
			}
		end

		for n, str in pairs(strings) do
			if player == "RAID" or player == "GUILD" or player == "PARTY" then -- note the upper case
				JBP:SendCommMessage("JBP", str, player, nil, "BULK", EDITBOX.callback, {n, #strings})
			else
				JBP:SendCommMessage("JBP", str, "WHISPER", player, "BULK", EDITBOX.callback, {n, #strings})
			end
		end
	end
	
	JBP.DD:CloseDropDownMenus()
end

function Comm:HandleTopLevelMenu()
	local info = JBP.DD:CreateInfo()
	info.notCheckable = true
	info.hasArrow = true


	info.text = RAID
	info.disabled = not IsInRaid()
	info.value = function() self.player = "RAID"; ExportDestination.HandleTopLevelMenu(self) end
	JBP.DD:AddButton(info)


	info.text = PARTY
	info.disabled = not IsInGroup()
	info.value = function() self.player = "PARTY"; ExportDestination.HandleTopLevelMenu(self) end
	JBP.DD:AddButton(info)


	info.text = GUILD
	info.disabled = not IsInGuild()
	info.value = function() self.player = "GUILD"; ExportDestination.HandleTopLevelMenu(self) end
	JBP.DD:AddButton(info)


	local targetIsXrealm = UnitRealmRelationship("target") == LE_REALM_RELATION_COALESCED 
	info.text = TARGET .. ": " .. (GetUnitName("target", true) or NONE)
	-- can't send cross realm right now. messages appear to send, but are never recieved.
	info.disabled = not UnitName("target") or targetIsXrealm
	if targetIsXrealm then
		info.tooltipWhileDisabled = true
		info.tooltipTitle = TARGET
		info.tooltipText = ERR_PETITION_NOT_SAME_SERVER
	end
	info.value = function() self.player = GetUnitName("target", true); ExportDestination.HandleTopLevelMenu(self) end
	JBP.DD:AddButton(info)


	info.text = strtrim(EDITBOX:GetText())
	local player = strtrim(EDITBOX:GetText())
	local playerLength = strlenutf8(player)
	info.disabled = (strfind(player, "[`~^%d!@#%$%%&%*%(%)%+=_]") or playerLength <= 1 or playerLength > 35) and true
	info.value = function() self.player = player; ExportDestination.HandleTopLevelMenu(self) end
	local text = L["EXPORT_TOCOMM"]
	if not info.disabled then
		text = text .. ": " .. player
	end
	info.tooltipWhileDisabled = true
	info.tooltipTitle = text
	if player:find("%-") then
		text = "|TInterface\\AddOns\\JustBecomePro\\Textures\\Alert:0:2|t" .. text
		info.tooltipText = ERR_PETITION_NOT_SAME_SERVER
	else
		info.tooltipText = L["EXPORT_TOCOMM_DESC"]

	end
	info.text = text
	JBP.DD:AddButton(info)
end

function Comm:SetButtonAttributes(editbox, info)
	info.text = L["EXPORT_TOCOMM"]
	info.tooltipTitle = L["EXPORT_TOCOMM"]
	info.hasArrow = true
end








-- -----------------------
-- DROPDOWN
-- -----------------------

local CurrentHandler
function JBP.IE:ImportExport_DropDown(...)
	local DROPDOWN = self
	EDITBOX = DROPDOWN:GetParent()
	JBP.IE.ImportExport_EditBox = EDITBOX

	local VALUE = JBP.DD.MENU_VALUE

	if JBP.DD.MENU_LEVEL == 1 then
		CurrentHandler = nil
	elseif JBP.DD.MENU_LEVEL == 2 then
		assert(type(VALUE) == "table")
		CurrentHandler = VALUE
	end
	
	JBP:Fire("JBP_CONFIG_IMPORTEXPORT_DROPDOWNDRAW", CurrentHandler)
	
	if JBP.DD.MENU_LEVEL == 2 then
		VALUE:HandleTopLevelMenu()

	elseif JBP.DD.MENU_LEVEL == 1 then

		----------IMPORT----------
		
		-- heading
		local info = JBP.DD:CreateInfo()
		info.text = L["IMPORT_HEADING"]
		info.isTitle = true
		info.notCheckable = true
		JBP.DD:AddButton(info)

		-- List of Import Sources
		for k, importSource in pairs(ImportSource.instances) do
			local info = JBP.DD:CreateInfo()
			info.text = get(importSource.displayText, EDITBOX)
			
			if importSource.displayDescription then
				info.tooltipTitle = get(importSource.displayText, EDITBOX)
				info.tooltipText = importSource.displayDescription
				info.tooltipWhileDisabled = true
			end
			
			info.value = importSource
			info.notCheckable = true
			info.disabled = get(importSource.displayDisabled, EDITBOX)
			info.hasArrow = not info.disabled
			JBP.DD:AddButton(info)
		end


		JBP.DD:AddSpacer()



		----------EXPORT----------

		-- heading
		info = JBP.DD:CreateInfo()
		info.text = L["EXPORT_HEADING"]
		info.isTitle = true
		info.notCheckable = true
		JBP.DD:AddButton(info)
		
		-- List of export destinations
		for k, exportDestination in pairs(ExportDestination.instances) do
			local info = JBP.DD:CreateInfo()
			info.tooltipWhileDisabled = true
			info.notCheckable = true
			
			exportDestination:SetButtonAttributes(EDITBOX, info)
			
			info.value = exportDestination
			
			JBP.DD:AddButton(info)
		end
		
	elseif type(VALUE) == "table" then
		if VALUE.class == Item then
			VALUE:BuildChildMenu()
		elseif VALUE.class == Bundle then
			VALUE:Evaluate()
		else
			error("Bad value at " .. JBP.DD.MENU_LEVEL)
		end
	elseif type(VALUE) == "function" then
		VALUE()
	end
end








