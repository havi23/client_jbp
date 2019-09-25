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
	

local MapConditionObjectToEventSettings = {}

local Module = JBP:NewClass("IconModule_IconEventConditionHandler", "IconModule")
Module:SetAllowanceForType("", false)
Module.dontInherit = true

Module:RegisterIconEvent(3, "OnCondition", {
	category = L["EVENT_CATEGORY_CONDITION"],
	text = L["SOUND_EVENT_ONCONDITION"],
	desc = L["SOUND_EVENT_ONCONDITION_DESC"],
	settings = {
		IconEventOnCondition = true,
	},
})

Module:PostHookMethod("OnImplementIntoIcon", function(self, icon)
	local EventHandlersSet = icon.EventHandlersSet
	
	if EventHandlersSet.OnCondition then
		self:Enable()
	else
		self:Disable()
	end
end)

local function JBP_CNDT_OBJ_PASSING_CHANGED(event, ConditionObject, failed)
	if not failed then
		local matches = MapConditionObjectToEventSettings[ConditionObject]
		if matches then
			for eventSettings, icon in pairs(matches) do
				icon:QueueEvent(eventSettings.__proxyRef)
				icon:ProcessQueuedEvents()
			end
		end
	end
end

function Module:OnEnable()
	local icon = self.icon
	
	for _, eventSettings in JBP:InNLengthTable(icon.Events) do
		if eventSettings.Event == "OnCondition" then
			local ConditionObjectConstructor = icon:Conditions_GetConstructor(eventSettings.OnConditionConditions)
			local ConditionObject = ConditionObjectConstructor:Construct()
		
			if ConditionObject then
				ConditionObject:RequestAutoUpdates(eventSettings, true)
				
				local matches = MapConditionObjectToEventSettings[ConditionObject]
				if not matches then
					matches = {}
					MapConditionObjectToEventSettings[ConditionObject] = matches
				end
				matches[JBP.C.EventHandler:Proxy(eventSettings, icon)] = icon
				
				JBP:RegisterCallback("JBP_CNDT_OBJ_PASSING_CHANGED", JBP_CNDT_OBJ_PASSING_CHANGED)
			end
		end
	end
end

function Module:OnDisable()
	for ConditionObject, matches in pairs(MapConditionObjectToEventSettings) do
		for eventSettings, icon in pairs(matches) do
			if icon == self.icon then
				ConditionObject:RequestAutoUpdates(eventSettings, false)
				matches[eventSettings] = nil
			end
		end
	end
end


JBP:RegisterCallback("JBP_GLOBAL_UPDATE", function()
	JBP:UnregisterCallback("JBP_CNDT_OBJ_PASSING_CHANGED", JBP_CNDT_OBJ_PASSING_CHANGED)
end)




do
	local CNDT = JBP.CNDT
	
	
	local ConditionSet = {
		parentSettingType = "iconEventHandler",
		parentDefaults = JBP.Icon_Defaults.Events["**"],
		
		settingKey = "OnConditionConditions",
		GetSettings = function(self)
			local currentEventID = JBP.EVENTS.currentEventID
			if currentEventID then
				return JBP.CI.ics.Events[currentEventID].OnConditionConditions
			end
		end,
		
		iterFunc = JBP.EVENTS.InIconEventSettings,
		iterArgs = {JBP.EVENTS},

		useDynamicTab = true,
		ShouldShowTab = function(self)
			local button = JustBecomePro_IconEditor.Pages.Events.EventSettingsContainer.IconEventOnCondition
			
			return button and button:IsShown()
		end,
		tabText = L["EVENTCONDITIONS"],
		tabTooltip = L["EVENTCONDITIONS_TAB_DESC"],
		
	}
	CNDT:RegisterConditionSet("IconEventOnCondition", ConditionSet)
	
end


