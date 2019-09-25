﻿-- --------------------
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


local Timer = JBP.C.EventHandler:New("Timer", 51)

Timer:RegisterEventDefaults{
	Counter = "",
	CounterAmt = 1,
	TimerOperation = "start",
}



JBP:NewClass("Timer"){
	started = false,
	start = 0,
	durSum = 0,

	Reset = function(self)
		self.start = JBP.time
		self.durSum = 0
	end,
	Start = function(self)
		if not self.started then
			self.started = true
			self.start = JBP.time
		end
	end,
	Pause = function(self)
		if self.started then
			self.started = false
			self.durSum = self.durSum + (JBP.time - self.start)
		end
	end,
	Stop = function(self)
		self.started = false
		self:Reset()
	end,
	GetTime = function(self)
		return self.durSum + (self.started and (JBP.time - self.start) or 0)
	end,
}

local TIMERS = setmetatable({}, {__index = function(self, k)
	local t = JBP.C.Timer:New()
	self[k] = t
	return t
end})

JBP.TIMERS = TIMERS

function Timer:SanitizeTimerName(counter)
	-- don't return in a single line because that will return all of gsub's return values, which we don't want.
	counter = tostring(counter):trim():lower():gsub("[ \t\r\n]", "")
	return counter
end

-- Required methods
function Timer:ProcessIconEventSettings(event, eventSettings)
	return eventSettings.Counter ~= ""
end

function Timer:HandleEvent(icon, eventSettings)
	local Counter = eventSettings.Counter
	local TimerOperation = eventSettings.TimerOperation

	if TimerOperation == "reset" then
		TIMERS[Counter]:Reset()
	elseif TimerOperation == "start" then
		TIMERS[Counter]:Start()
	elseif TimerOperation == "restart" then
		TIMERS[Counter]:Reset()
		TIMERS[Counter]:Start()
	elseif TimerOperation == "pause" then
		TIMERS[Counter]:Pause()
	elseif TimerOperation == "stop" then
		TIMERS[Counter]:Stop()
		
	else
		JBP:Error("Bad timer operation: " .. tostring(icon) .. " " .. Counter .. ": " .. TimerOperation)
		return
	end
	
	JBP:Fire("JBP_TIMER_MODIFIED", Counter)

	return true
end

function Timer:OnRegisterEventHandlerDataTable()
	error("The Timer event handler does not support registration of event handler data - everything is user-defined.", 3)
end



local ConditionCategory = JBP.CNDT:GetCategory("MISC")

ConditionCategory:RegisterCondition(0.51,	"TIMER", {
	text = L["EVENTHANDLER_TIMER_TAB"],
	tooltip = L["CONDITIONPANEL_TIMER_DESC"],
	min = 0,
	range = 30,
	step = 0.1,
	formatter = JBP.C.Formatter.TIME_YDHMS,

	unit = false,
	icon = "Interface\\Icons\\spell_mage_altertime",
	name = function(editbox)
		editbox:SetTexts(L["CONDITION_TIMER"], L["CONDITION_TIMER_EB_DESC"])
	end,
	useSUG = "timerName",
	tcoords = JBP.CNDT.COMMON.standardtcoords,
	Env = {
		TIMERS = TIMERS,
	},
	funcstr = function(c, icon)
		local timer = format("%q", Timer:SanitizeTimerName(c.Name))

		return "TIMERS[" .. timer .. "]:GetTime() c.Operator c.Level"
	end,
	events = function(ConditionObject, c)
		return
			ConditionObject:GenerateNormalEventString("JBP_TIMER_MODIFIED", Timer:SanitizeTimerName(c.Name))
	end,
	anticipate = function(c)
		local timer = format("%q", Timer:SanitizeTimerName(c.Name))

		return [[
			local timer = TIMERS[]] .. timer .. [[]
			local VALUE = not timer.started and huge or (time + (c.Level - timer:GetTime()))
		]]
	end,
})



local DogTag = LibStub("LibDogTag-3.0", true)
if DogTag then
	DogTag:AddTag("JBP", "Timer", {
		code = function(timername)
			return TIMERS[Timer:SanitizeTimerName(timername)]:GetTime()
		end,
		arg = {
			'timername', 'string', '@req',
		},
		ret = "number",
		doc = L["DT_DOC_Timer"],
		example = '[Timer("timername")] => "3"',
		events = "FastUpdate",
		category = L["MISCELLANEOUS"],
	})
end