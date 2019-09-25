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

local floor, min, max, strsub, strfind = 
	  floor, min, max, strsub, strfind
local pairs, ipairs, sort, tremove, CopyTable = 
	  pairs, ipairs, sort, tremove, CopyTable
	  
local CI = JBP.CI

local LSM = LibStub("LibSharedMedia-3.0")

-- GLOBALS: CreateFrame, NORMAL_FONT_COLOR



local EVENTS = JBP.EVENTS
local Sound = JBP.EVENTS:GetEventHandler("Sound")

Sound.handlerName = L["SOUND_TAB"]
Sound.handlerDesc = L["SOUND_TAB_DESC"]
Sound.LSM = LSM

JBP.HELP:NewCode("SND_INVALID_CUSTOM")


JBP:RegisterCallback("JBP_OPTIONS_LOADED", function()	
	local ConfigContainer = Sound.ConfigContainer
	ConfigContainer.SoundList.frames = {}

	
	ConfigContainer.Header:SetText(L["SOUND_SOUNDTOPLAY"])
end)



function Sound:GetFrame(id)
	local SoundList = self.ConfigContainer.SoundList
	local frames = SoundList.frames

	if frames[id] then
		return frames[id]
	end
	
	local frame = JBP.C.Config_CheckButton:New("CheckButton", nil, SoundList, "JustBecomePro_SoundSelectButton", id)
	frames[id] = frame

	if id == 1 then
		frame:SetPoint("TOP", 0, 0)
	else
		frame:SetPoint("TOP", frames[id-1], "BOTTOM", 0, 0)
	end

	return frame
end


---------- Events ----------
function Sound:LoadSettingsForEventID(id)
	self:SelectSound(EVENTS:GetEventSettings().Sound)

	self.ConfigContainer:RequestReload()
end

function Sound:GetEventDisplayText(eventID)
	if not eventID then return end

	local name = EVENTS:GetEventSettings(eventID).Sound

	if name == "None" then
		name = "|cff808080" .. NONE
	end

	return ("|cffcccccc" .. self.handlerName .. ":|r " .. name)
end



---------- Sounds ----------
local soundSorter = function(a, b)
	local JBPa = strsub(a, 1, 3) == "JBP"
	local JBPb = strsub(b, 1, 3) == "JBP"
	if JBPa or JBPb then
		if JBPa and JBPb then
			return a < b
		else
			return JBPa
		end
	else
		return a < b
	end
end
function Sound:CompileSoundList()
	if not Sound.List or #LSM:List("sound")-1 ~= #Sound.List then
		Sound.List = CopyTable(LSM:List("sound"))

		-- We'll just put this back at the end instead of trying to sort it.
		JBP.tDeleteItem(Sound.List, "None")

		sort(Sound.List, soundSorter)

		tinsert(Sound.List, 1, "None")
	end
end

function Sound:SetupSoundList()
	self:CompileSoundList()

	for i = 1, #Sound.List do
		local soundName = Sound.List[i]
		local frame = self:GetFrame(i)

		frame.soundName = soundName
		frame.Name:SetText(soundName)
		frame:SetSetting("Sound", soundName)
		frame.soundFile = LSM:Fetch("sound", soundName)
		if soundName == "None" then
			-- No need to show this if the sound isn't none. None will always be #1.
			frame.Play:Hide()
		end
		frame:Show()
	end
	
	local frames = self.ConfigContainer.SoundList.frames
	for i = #Sound.List + 1, #frames do
		frames[i]:Hide()
	end
end

function Sound:SelectSound(name)
	if not name then return end

	self:SetupSoundList()

	local listID = JBP.tContains(Sound.List, name)

	if listID then
		local soundFrame = self:GetFrame(listID)
		self.ConfigContainer.SoundList.ScrollFrame:ScrollToFrame(soundFrame)
	end
end



---------- Tests ----------
local soundChannels = {
	-- GLOBALS: SOUND_VOLUME, MUSIC_VOLUME, AMBIENCE_VOLUME, DIALOG_VOLUME
	SFX = {
		text = ENABLE_SOUNDFX,
		enableCVar = "Sound_EnableSFX",
		volumeCVar = "Sound_SFXVolume",
	},
	Music = {
		text = MUSIC_VOLUME,
		enableCVar = "Sound_EnableMusic",
		volumeCVar = "Sound_MusicVolume",
	},
	Ambience = {
		text = AMBIENCE_VOLUME,
		enableCVar = "Sound_EnableAmbience",
		volumeCVar = "Sound_AmbienceVolume",
	},
	Dialog = {
		text = DIALOG_VOLUME,
		enableCVar = "Sound_EnableDialog",
		volumeCVar = "Sound_DialogVolume",
	},
	Master = {
		text = MASTER_VOLUME,
		enableCVar = "Sound_EnableAllSound",
		volumeCVar = "Sound_MasterVolume",
	},
}

JBP.HELP:NewCode("SOUND_TEST_ERROR", 10, false)

function Sound:TestSound(helpAnchor, settingValue)
	local error

	local success, err = pcall(Sound.PlaySoundFromSettingValue, Sound, settingValue)
	if not success then
		
		-- Remove the file name and line number from the error:
		err = gsub(err, ".-%.lua:%d+:%s*", "")

		if err:find("Invalid fileDataID") then
			err = err .. "\n\n" .. L["SOUND_ERROR_BADFILE"]
		end

		error = err

	elseif GetCVar("Sound_EnableAllSound") == "0" then
		error = L["SOUND_ERROR_ALLDISABLED"]
	else
		local channelData = soundChannels[JBP.db.profile.SoundChannel]

		if GetCVar(channelData.enableCVar) == "0" then
			error = L["SOUND_ERROR_DISABLED"]:format(channelData.text)
		elseif GetCVar(channelData.volumeCVar) == "0" then
			error = L["SOUND_ERROR_MUTED"]:format(channelData.text)
		end
	end

	if error then
		JBP.HELP:Show{
			code = "SOUND_TEST_ERROR",
			icon = JBP.CI.icon,
			relativeTo = helpAnchor,
			x = 0,
			y = 0,
			text = error
		}
	else 
		JBP.HELP:Hide("SOUND_TEST_ERROR")
	end
end



