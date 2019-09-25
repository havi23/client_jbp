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

local get = JBP.get

local EVENTS = JBP.EVENTS
local IE = JBP.IE


EVENTS.CONST = {
	EVENT_INVALID_REASON_MISSINGHANDLER = 1,
	EVENT_INVALID_REASON_MISSINGCOMPONENT = 2,
	EVENT_INVALID_REASON_MISSINGEVENT = 3,
	EVENT_INVALID_REASON_NOEVENT = 4,
}

local EventsTab = JBP.IE:RegisterTab("ICON", "ICONEVENTS", "Events", 10)
EventsTab:SetHistorySet(JBP.C.HistorySet:GetHistorySet("ICON"))
EventsTab:SetTexts(L["EVENTS_TAB"], L["EVENTS_TAB_DESC"])



---------- Icon Dragger ----------
JBP.IconDragger:RegisterIconDragHandler(120, -- Copy Event Handlers
	function(IconDragger, info)
		local n = IconDragger.srcicon:GetSettings().Events.n

		if IconDragger.desticon and n > 0 then
			info.text = L["ICONMENU_COPYEVENTHANDLERS"]:format(n)
			info.tooltipTitle = info.text
			info.tooltipText = L["ICONMENU_COPYEVENTHANDLERS_DESC"]:format(
				IconDragger.srcicon:GetIconName(true), n, IconDragger.desticon:GetIconName(true))
			
			return true
		end
	end,
	function(IconDragger)
		-- copy the settings
		local srcics = IconDragger.srcicon:GetSettings()
		
		IconDragger.desticon:GetSettings().Events = JBP:CopyWithMetatable(srcics.Events)
	end
)



function EVENTS:LoadConfig()
	local EventHandlerFrames = EVENTS.EventHandlerFrames
	EventHandlerFrames.frames = EventHandlerFrames.frames or {} -- Framestack workaround
	local frames = EventHandlerFrames.frames

	local previousFrame

	local yAdjustTitle, yAdjustText = 0, 0
	local locale = GetLocale()
	if locale == "zhCN" or locale == "zhTW" then
		yAdjustTitle, yAdjustText = 3, -3
	end

	
	local oldID = max(1, EVENTS.currentEventID or 1)

	local didLoad
	for i = 1, JBP.CI.ics.Events.n do
		-- This wizard magic allows us to iterate over all eventIDs, 
		-- starting with the currently selected one (oldID)
		-- So, for example, if oldID == 3 and JBP.CI.ics.Events.n == 6,
		-- eventID will be iterated as 3, 4, 5, 6, 1, 2
		local eventID = ((i-2+oldID) % JBP.CI.ics.Events.n) + 1
		i = nil -- i should not be used after this point since it won't correspond to any meaningful data.


		-- Get the frame that this event will be listed in.
		local frame = frames[eventID]
		if not frame then
			-- If the frame doesn't exist, then create it.
			frame = CreateFrame("CheckButton", nil, EventHandlerFrames, "JustBecomePro_Event", eventID)
			frames[eventID] = frame

			if previousFrame then
				frame:SetPoint("TOPLEFT", previousFrame, "BOTTOMLEFT", 0, -2)
				frame:SetPoint("TOPRIGHT", previousFrame, "BOTTOMRIGHT", 0, -2)
			end

			local p, t, r, x, y = frame.EventName:GetPoint(1)
			frame.EventName:SetPoint(p, t, r, x, y + yAdjustTitle)
			local p, t, r, x, y = frame.EventName:GetPoint(2)
			frame.EventName:SetPoint(p, t, r, x, y + yAdjustTitle)

			local p, t, r, x, y = frame.DataText:GetPoint(1)
			frame.DataText:SetPoint(p, t, r, x, y + yAdjustText)
			local p, t, r, x, y = frame.DataText:GetPoint(2)
			frame.DataText:SetPoint(p, t, r, x, y + yAdjustText)

			frame.DataText:SetWordWrap(false)
		end
		previousFrame = frame
		frame:Show()


		-- Check if this eventID is valid, and load it if it is.
		local isValid, reason = EVENTS:IsEventIDValid(eventID)
		local eventSettings = EVENTS:GetEventSettings(eventID)
		local EventHandler = EVENTS:GetEventHandlerForEventSettings(eventSettings)
		local eventData = JBP.EventList[eventSettings.Event]

		
		-- If we have the event's data, set the event name of the frame to the localized name of the event.
		-- If we don't have the event's data, set the event name of the raw identifier of the event.
		if eventData then
			frame.EventName:SetText(eventID .. ") " .. eventData.text)
		else
			frame.EventName:SetText(eventID .. ") " .. eventSettings.Event)
		end

		if isValid then
			-- The event is valid and all needed components were found,
			-- so set up the button.

			frame:Enable()


			frame.event = eventData.event
			frame.eventData = eventData

			local desc = eventData.desc .. "\r\n\r\n" .. L["EVENTS_HANDLERS_GLOBAL_DESC"]
			JBP:TT(frame, eventData.text, desc, 1, 1)


			-- This delegates the setup of frame.DataText to the event handler
			-- so that it can put useful information about the user's settings
			-- (e.g. "Sound: JBP - Pling3" or "Animation: Icon: Shake")
			local EventHandler = EVENTS:GetEventHandlerForEventSettings(eventID)

			local dataText = EventHandler:GetEventDisplayText(eventID)
			frame.DataText:SetText(dataText)

			if EventHandler.testable then
				frame.Play:Enable()
			else
				frame.Play:Disable()
			end

			-- If we have not yet loaded an event for this configuration load,
			-- then load this event. The proper event settings and event handler
			-- configuration will be shown and setup with stored settings.
			-- This is the reason why we start with the currently selected eventID.
			if not didLoad then
				EVENTS:LoadEventID(eventID)
				didLoad = true
			end

		else
			frame:Disable()
			JBP:TT(frame, nil, nil)

			if reason == EVENTS.CONST.EVENT_INVALID_REASON_MISSINGHANDLER then
				-- The handler (E.g. Sound, Animation, etc.) of the event settings was not found.
				frame.DataText:SetText("|cFFFF5050UNKNOWN HANDLER:|r " .. tostring(EVENTS:GetEventSettings(eventID).Type))

			elseif reason == EVENTS.CONST.EVENT_INVALID_REASON_MISSINGEVENT then
				-- The event (E.g. "OnSomethingHappened") was not found
				frame.DataText:SetText("|cFFFF5050UNKNOWN EVENT|r")

			elseif reason == EVENTS.CONST.EVENT_INVALID_REASON_NOEVENT then
				-- The handler is unconfigured
				-- This is a non-critical error, so we format the error message nicely for the user.
				frame.DataText:SetText(L["SOUND_EVENT_NOEVENT"])
				frame:Enable()

			elseif reason == EVENTS.CONST.EVENT_INVALID_REASON_MISSINGCOMPONENT then
				-- The event was found, but it is not available for the current icon's configuration.
				-- This is a non-critical error, so we format the error message nicely for the user.
				frame.DataText:SetText(L["SOUND_EVENT_DISABLEDFORTYPE"])
				JBP:TT(frame, eventData.text, L["SOUND_EVENT_DISABLEDFORTYPE_DESC2"]:format(JBP.Types[JBP.CI.ics.Type].name), 1, 1)
			end
		end
	end

	-- Hide unused frames
	for i = max(JBP.CI.ics.Events.n + 1, 1), #frames do
		frames[i]:Hide()
	end

	-- Position the first frame
	if frames[1] then
		frames[1]:SetPoint("TOPLEFT", EventHandlerFrames, "TOPLEFT", 0, 0)
		frames[1]:SetPoint("TOPRIGHT", EventHandlerFrames, "TOPRIGHT", 0, 0)
	end

	-- Set the height of the container 
	local frame1Height = frames[1] and frames[1]:GetHeight() or 0
	EventHandlerFrames:SetHeight(max(JBP.CI.ics.Events.n*frame1Height, 1))

	-- If an event handler's configuration was not loaded for an event,
	-- hide all handler configuration panels
	if not didLoad then
		EVENTS:ShowHandlerPickerButtons()
	end

	EVENTS:SetTabText()
end

function EVENTS:LoadEventID(eventID)

	JBP.IE:SaveSettings()
	
	EVENTS.currentEventID = eventID ~= 0 and eventID or nil


	-- RESET CONFIGURATION:
	-- Uncheck all existing notification handlers
	for i, frame in ipairs(EVENTS.EventHandlerFrames.frames) do
		frame:SetChecked(false)
	end

	-- Hide the config containers for all handlers
	for _, EventHandler in pairs(JBP.Classes.EventHandler.instancesByName) do
		EventHandler.ConfigContainer:Hide()
	end
	EVENTS.EventSettingsContainer:Hide()


	local eventFrame = eventID and EVENTS.EventHandlerFrames.frames[eventID]

	if not eventFrame or eventID == 0 or not eventFrame:IsShown() then
		return
	end

	-- START LOADING NEW EVENT:
	-- Check the corresponding notification handler list frame.
	eventFrame:SetChecked(true)

	EVENTS:HidePickerButtons()
	
	local EventHandler = EVENTS:GetEventHandlerForEventSettings(eventID)
	if EventHandler then
		EVENTS.EventSettingsContainer:Show()
		EventHandler.ConfigContainer:Show()
		
		EVENTS.currentEventHandler = EventHandler
		
		EventHandler:LoadSettingsForEventID(eventID)
		EVENTS:LoadEventSettings()
	end

end

function EVENTS:LoadEventSettings()
	local EventSettingsContainer = EVENTS.EventSettingsContainer

	if not EVENTS.currentEventID then
		EventSettingsContainer:Hide()
		return
	end

	local eventSettings = EVENTS:GetEventSettings()
	local EventHandler = EVENTS:GetEventHandlerForEventSettings(eventSettings)

	EventSettingsContainer:Show()

	-- Hide all settings frames
	for k, v in pairs(EventSettingsContainer) do
		if type(v) == "table" and v:GetParent() == EventSettingsContainer then
			v:Hide()
		end
	end

	local eventData = EVENTS:GetEventData()

	if eventData then
		IE.Pages.Events.EventSettingsEventName:SetText("(" .. EVENTS.currentEventID .. ") " .. eventData.text)

		if eventSettings.Event == "WCSP" then
			if EventHandler.frequencyMinimum then
				EventSettingsContainer.Frequency:Show()

				EventSettingsContainer.Frequency:SetMinMaxValues(EventHandler.frequencyMinimum, math.huge)
				EventSettingsContainer.Frequency:RequestReload()
			end
		else
			EventSettingsContainer.PassThrough:Show()
			EventSettingsContainer.OnlyShown:Show()
		end

		--load settings
		EventSettingsContainer.Value:SetText(eventSettings.Value)
		

		local settingsUsedByEvent = eventData.settings

		--show settings as needed
		for setting, frame in pairs(EventSettingsContainer) do
			if type(frame) == "table" then
				local state = settingsUsedByEvent and settingsUsedByEvent[setting]

				if type(state) == "function" then
					state(frame)
				else
					frame:Enable()
				end
				if state ~= nil then
					frame:SetShown(not not state)
				end
			end
		end

		-- EventSettingsContainer.PassingCndt:RequestReload()
		if EventSettingsContainer.PassingCndt				:GetChecked() then
			EventSettingsContainer.Operator.ValueLabel		:SetFontObject(GameFontHighlight)
			EventSettingsContainer.Operator					:Enable()
			EventSettingsContainer.Value					:Enable()
			if settingsUsedByEvent and type(settingsUsedByEvent.CndtJustPassed) ~= "function" then
				EventSettingsContainer.CndtJustPassed		:Enable()
			end
		else
			EventSettingsContainer.Operator.ValueLabel		:SetFontObject(GameFontDisable)
			EventSettingsContainer.Operator					:Disable()
			EventSettingsContainer.Value					:Disable()
			EventSettingsContainer.CndtJustPassed			:Disable()
		end

		EventSettingsContainer.Operator.ValueLabel:SetText(eventData.valueName)
		EventSettingsContainer.Value.ValueLabel:SetText(eventData.valueSuffix)

		local v = EventSettingsContainer.Operator:SetUIDropdownText(eventSettings.Operator, JBP.operators)
		if v then
			JBP:TT(EventSettingsContainer.Operator, v.tooltipText, nil, 1)
		end
	end

	JBP:Fire("JBP_CONFIG_EVENTS_SETTINGS_SETUP_POST")
end



function EVENTS:LoadHandlerPickerButtons()
	local previousFrame

	-- Handler pickers
	local HandlerPickers = IE.Pages.Events.HandlerPickers
	HandlerPickers.frames = HandlerPickers.frames or {} -- Framestack workaround

	for i, EventHandler in ipairs(JBP.Classes.EventHandler.orderedInstances) do

		local frame = HandlerPickers.frames[i]
		if not frame then
			-- If the frame doesn't exist, then create it.
			frame = CreateFrame("Button", nil, HandlerPickers, "JustBecomePro_HandlerPicker", i)
			HandlerPickers.frames[i] = frame

			if i == 1 then
				frame:SetPoint("TOP")
			else
				frame:SetPoint("TOP", previousFrame, "BOTTOM", 0, -10)
			end
		end

		frame.handlerIdentifier = EventHandler.identifier
		frame.Title:SetText(EventHandler.handlerName)
		frame.Desc:SetText(EventHandler.handlerDesc or "<No Description>")

		JBP:TT(frame, EventHandler.handlerName, "EVENTS_HANDLER_ADD_DESC", 1, nil)

		previousFrame = frame
	end
end

function EVENTS:LoadEventPickerButtons()
	local previousFrame

	-- Event (Trigger) pickers
	local EventPickers = IE.Pages.Events.EventPickers
	EventPickers.frames = EventPickers.frames or {} -- Framestack workaround
	
	for i, frame in ipairs(EventPickers.frames) do
		frame:Hide()
	end

	local EventHandler = EVENTS:GetEventHandler(EVENTS.pickedHandler)

	for i, eventData in ipairs(EVENTS:GetValidEvents(EventHandler)) do

		local frame = EventPickers.frames[i]
		if not frame then
			-- If the frame doesn't exist, then create it.
			frame = CreateFrame("Button", nil, EventPickers, "JustBecomePro_EventPicker", i)
			EventPickers.frames[i] = frame
		end

		frame.Header:SetText(eventData.category)

		if i == 1 then
			frame:SetPoint("TOP", 0, -18)
		else
			if EventPickers.frames[i-1].Header:GetText() ~= eventData.category then
				frame:SetPoint("TOP", previousFrame, "BOTTOM", 0, -20)
				frame.Header:Show()
			else
				frame:SetPoint("TOP", previousFrame, "BOTTOM", 0, -1)
				frame.Header:Hide()
			end
		end

		frame:Show()
		frame.event = eventData.event
		frame.Title:SetText(get(eventData.text))
		JBP:TT(frame, eventData.text, eventData.desc, 1, 1)

		previousFrame = frame
	end
end

function EVENTS:ShowHandlerPickerButtons()
	EVENTS.pickedHandler = nil

	EVENTS:LoadHandlerPickerButtons()
	EVENTS:LoadEventID(nil)

	IE.Pages.Events.AddEvent:SetChecked(true)

	IE.Pages.Events.HandlerPickers:Show()
	IE.Pages.Events.EventPickers:Hide()
end

function EVENTS:ShowEventPickerButtons()
	EVENTS:LoadEventPickerButtons()

	IE.Pages.Events.HandlerPickers:Hide()
	IE.Pages.Events.EventPickers:Show()
end 

function EVENTS:HidePickerButtons()
	IE.Pages.Events.AddEvent:SetChecked(false)

	IE.Pages.Events.HandlerPickers:Hide()
	IE.Pages.Events.EventPickers:Hide()
end

function EVENTS:PickEvent(event)
	local handlerIdentifier = EVENTS.pickedHandler

	JBP.CI.ics.Events.n = JBP.CI.ics.Events.n + 1

	local eventID = JBP.CI.ics.Events.n
	local eventSettings = EVENTS:GetEventSettings(eventID)

	eventSettings.Type = handlerIdentifier

	EVENTS:SetEvent(eventID, event)

	EVENTS.currentEventID = eventID
	IE.Pages.Events:OnSettingSaved()
end

function EVENTS:SetEvent(eventID, event)
	local eventSettings = EVENTS:GetEventSettings(eventID)

	eventSettings.Event = event

	local eventData = JBP.EventList[event]
	if eventData and eventData.applyDefaultsToSetting then
		eventData.applyDefaultsToSetting(eventSettings)
	end

	IE.Pages.Events:OnSettingSaved()
end




function EVENTS:AdjustScrollFrame()
	local ScrollFrame = EVENTS.EventHandlerFrames.ScrollFrame
	local eventFrame = EVENTS.EventHandlerFrames.frames[EVENTS.currentEventID]

	if not eventFrame then return end

	ScrollFrame:ScrollToFrame(eventFrame)
end

function EVENTS:SetTabText()
	local n = EVENTS:GetNumUsedEvents()

	if n > 0 then
		EventsTab:SetText(L["EVENTS_TAB"] .. ": |cFFFF5959" .. n)
	else
		EventsTab:SetText(L["EVENTS_TAB"] .. ": 0")
	end
end
JBP:RegisterCallback("JBP_CONFIG_TAB_CLICKED", EVENTS, "SetTabText")



function EVENTS:IsEventIDValid(eventID)
	local eventSettings = EVENTS:GetEventSettings(eventID)

	local EventHandler = EVENTS:GetEventHandlerForEventSettings(eventSettings)

	local validEvents = EVENTS:GetValidEvents(EventHandler)


	if eventSettings.Event == "" then
		-- The event is not set
		return false, EVENTS.CONST.EVENT_INVALID_REASON_NOEVENT

	elseif not JBP.EventList[eventSettings.Event] then
		-- The event does not exist
		return false, EVENTS.CONST.EVENT_INVALID_REASON_MISSINGEVENT
		
	end

	if validEvents[eventSettings.Event] then
		if EventHandler then
			-- This event is valid and can be loaded
			return true, 0
		else
			-- The event handler could not be found
			return false, EVENTS.CONST.EVENT_INVALID_REASON_MISSINGHANDLER
		end
	else
		-- The event is not valid for the current icon configuration
		return false, EVENTS.CONST.EVENT_INVALID_REASON_MISSINGCOMPONENT
	end
end

function EVENTS:GetEventSettings(eventID)
	eventID = eventID or EVENTS.currentEventID
	local Events = JBP.CI.ics and JBP.CI.ics.Events

	if Events and eventID and eventID <= Events.n then
		return Events[eventID]
	end
end

function EVENTS:GetEventData(event)
	if not event then
		event = EVENTS:GetEventSettings().Event
	end

	return JBP.EventList[event]
end

function EVENTS:GetNumUsedEvents()
	local n = 0

	if not JBP.CI.ics then
		return 0
	end

	for i, eventSettings in JBP:InNLengthTable(JBP.CI.ics.Events) do
		local Module = EVENTS:GetEventHandlerForEventSettings(eventSettings)

		if Module then
			local has = Module:ProcessIconEventSettings(eventSettings.Event, eventSettings)
			if has then
				n = n + 1
			end
		end
	end

	return n
end

function EVENTS:GetEventHandlerForEventSettings(arg1)
	local eventSettings
	if type(arg1) == "table" then
		eventSettings = arg1
	else
		eventSettings = EVENTS:GetEventSettings(arg1)
	end

	if eventSettings then
		return JBP.EVENTS:GetEventHandler(eventSettings.Type)
	end
end

function EVENTS:GetValidEvents(EventHandler)
	JBP:ValidateType("2 (EventHandler)", "EVENTS:GetValidEvents(EventHandler)", EventHandler, "EventHandler")

	local ValidEvents = EVENTS.ValidEvents
	
	ValidEvents = wipe(ValidEvents or {})
	
	for _, Component in ipairs(JBP.CI.icon.Components) do
		for _, eventData in ipairs(Component.IconEvents) do

			-- Don't include WhileConditionSetPassing if the event handler doesn't support it.
			if eventData.event ~= "WCSP" or EventHandler.supportWCSP then
				-- Put it in the table as an indexed field.
				ValidEvents[#ValidEvents+1] = eventData
				
				-- Put it in the table keyed by the event, for lookups.
				ValidEvents[eventData.event] = eventData
			end
		end
	end
	
	JBP:SortOrderedTables(ValidEvents)
	
	return ValidEvents
end


local function OperatorMenu_DropDown_OnClick(button, dropdown)
	dropdown:SetUIDropdownText(button.value)

	EVENTS:GetEventSettings().Operator = button.value
	JBP:TT(dropdown, button.tooltipTitle, nil, 1)

	dropdown:OnSettingSaved()
end
function EVENTS.OperatorMenu_DropDown(dropdown)
	local eventData = EVENTS.EventHandlerFrames.frames[EVENTS.currentEventID].eventData
	local eventSettings = EVENTS:GetEventSettings()

	for k, v in pairs(JBP.operators) do
		if not eventData.blacklistedOperators or not eventData.blacklistedOperators[v.value] then
			local info = JBP.DD:CreateInfo()
			info.func = OperatorMenu_DropDown_OnClick
			info.text = v.text
			info.value = v.value
			info.checked = v.value == eventSettings.Operator
			info.tooltipTitle = v.tooltipText
			info.arg1 = dropdown
			JBP.DD:AddButton(info)
		end
	end
end


local function ChangeEvent_Dropdown_OnClick(button, eventID, event)
	JBP.DD:CloseDropDownMenus()

	EVENTS:SetEvent(eventID, event)
end
local function ChangeEvent_Dropdown_OnClick_Clone(button, eventID)
	local eventSettings = EVENTS:GetEventSettings(eventID)

	local n = JBP.CI.ics.Events.n + 1
	JBP:CopyTableInPlaceUsingDestinationMeta(eventSettings, JBP.CI.ics.Events[n])
	JBP.CI.ics.Events.n = n

	JBP.DD:CloseDropDownMenus()

	IE.Pages.Events:OnSettingSaved()

	if EVENTS:IsEventIDValid(n) then
		EVENTS:LoadEventID(n)
	end
end
function EVENTS:ChangeEvent_Dropdown()
	local eventButton = self.eventButton -- This is set in XML when the dropdown is opened.
	local eventID = eventButton:GetID()
	local EventHandler = EVENTS:GetEventHandlerForEventSettings(eventID)

	if JBP.DD.MENU_LEVEL == 1 then		
		local info = JBP.DD:CreateInfo()
		info.text = L["EVENTS_CLONEHANDLER"]
		info.arg1 = eventID
		info.func = ChangeEvent_Dropdown_OnClick_Clone
		info.keepShownOnClick = false
		info.notCheckable = true
		JBP.DD:AddButton(info)

		local info = JBP.DD:CreateInfo()
		info.text = L["EVENTS_CHANGETRIGGER"]
		info.value = "CHANGE"
		info.hasArrow = true
		info.notCheckable = true
		JBP.DD:AddButton(info)

	elseif JBP.DD.MENU_VALUE == "CHANGE" then
		for _, eventData in ipairs(EVENTS:GetValidEvents(EventHandler)) do
			local info = JBP.DD:CreateInfo()

			info.text = get(eventData.text)
			info.tooltipTitle = get(eventData.text)
			info.tooltipText = get(eventData.desc)
			

			info.value = eventData.event
			info.checked = eventData.event == eventButton.event
			info.func = ChangeEvent_Dropdown_OnClick
			info.keepShownOnClick = false
			info.arg1 = eventButton:GetID()
			info.arg2 = eventData.event

			JBP.DD:AddButton(info)
		end
	end
end




local ColumnConfig = JBP.C.EventHandler_ColumnConfig

function ColumnConfig:GetListItemFrame(frameID)
	local SubHandlerList = self.ConfigContainer.SubHandlerList
	
	local frame = SubHandlerList[frameID]
	if not frame then
		frame = CreateFrame("CheckButton", SubHandlerList:GetName().."Item"..frameID, SubHandlerList, "JustBecomePro_EventHandler_SubHandlerListButton", frameID)
		SubHandlerList[frameID] = frame

		local previousFrame = frameID > 1 and SubHandlerList[frameID - 1] or nil
		if previousFrame then
			frame:SetPoint("TOPLEFT", previousFrame, "BOTTOMLEFT", 0, -2)
			frame:SetPoint("TOPRIGHT", previousFrame, "BOTTOMRIGHT", 0, -2)
		end
	end

	frame.EventHandler = self

	return frame
end


function ColumnConfig:GetSubHandler(eventID)
	local subHandlerIdentifier = EVENTS:GetEventSettings(eventID)[self.subHandlerSettingKey]
	local subHandlerData = self.AllSubHandlersByIdentifier[subHandlerIdentifier]

	return subHandlerData, subHandlerIdentifier
end

local subHandlersToDisplay = {}
function ColumnConfig:LoadSettingsForEventID(id)
	local SubHandlerList = self.ConfigContainer.SubHandlerList
		
	wipe(subHandlersToDisplay)
	
	for i, subHandlerDataParent in ipairs(self.NonSpecificEventHandlerData) do
		tinsert(subHandlersToDisplay, subHandlerDataParent)
	end
	
	for i, Component in ipairs(JBP.CI.icon.Components) do
		if  Component.EventHandlerData and Component.IsEnabled then
			for i, subHandlerDataParent in ipairs(Component.EventHandlerData) do
				if subHandlerDataParent.identifier == self.subHandlerDataIdentifier then
					tinsert(subHandlersToDisplay, subHandlerDataParent)
				end
			end
		end
	end
	
	JBP:SortOrderedTables(subHandlersToDisplay)
	
	local frameID = 0
	for _, subHandlerDataParent in ipairs(subHandlersToDisplay) do
		if not get(subHandlerDataParent.subHandlerData.hidden) then
			frameID = frameID + 1
			local frame = self:GetListItemFrame(frameID)
			frame:Show()

			local animationData = subHandlerDataParent.subHandlerData
			frame.subHandlerData = animationData
			frame.subHandlerIdentifier = animationData.subHandlerIdentifier

			frame.Name:SetText(animationData.text)
			JBP:TT(frame, animationData.text, animationData.desc, 1, 1)
		end
	end
	
	for i = #subHandlersToDisplay + 1, #SubHandlerList do
		SubHandlerList[i]:Hide()
	end

	if SubHandlerList[1] then
		SubHandlerList[1]:SetPoint("TOPLEFT", SubHandlerList, "TOPLEFT", 0, 0)
		SubHandlerList[1]:SetPoint("TOPRIGHT", SubHandlerList, "TOPRIGHT", 0, 0)
		
		SubHandlerList:Show()
	else
		SubHandlerList:Hide()
	end
	
	
	local EventSettings = EVENTS:GetEventSettings(id)
	self:SelectSubHandler(EventSettings[self.subHandlerSettingKey])
end

function ColumnConfig:SetSubHandler(subHandlerIdentifier)
	local subHandlerData = self.AllSubHandlersByIdentifier[subHandlerIdentifier]

	if JBP.CI.ics then
		local old = JBP.EVENTS:GetEventSettings()[self.subHandlerSettingKey]
		if old ~= subHandlerIdentifier then

			JBP.EVENTS:GetEventSettings()[self.subHandlerSettingKey] = subHandlerIdentifier

			local eventSettings = EVENTS:GetEventSettings()
			if subHandlerData.applyDefaultsToSetting then
				subHandlerData.applyDefaultsToSetting(eventSettings)
			end
			
			JBP.IE.Pages.Events:OnSettingSaved()
		end
	end
end

function ColumnConfig:SelectSubHandler(subHandlerIdentifier)
	local subHandlerListButton
	
	for i=1, #self.ConfigContainer.SubHandlerList do
		local f = self.ConfigContainer.SubHandlerList[i]
		if f and f:IsShown() then
			if f.subHandlerIdentifier == subHandlerIdentifier then
				f:SetChecked(true)
			else
				f:SetChecked(false)
			end
		end
	end

	local subHandlerData = self.AllSubHandlersByIdentifier[subHandlerIdentifier]
	self.currentSubHandlerData = subHandlerData

	self:SetupConfig(subHandlerData)
end

-- Override this method for handlers that need to blacklist a setting.
function ColumnConfig:IsFrameBlacklisted(frameName)
	return false
end

function ColumnConfig:SetupConfig(subHandlerData)
	local desiredFrames = subHandlerData.ConfigFrames
	local subHandlerIdentifier = subHandlerData.subHandlerIdentifier

	local EventSettings = EVENTS:GetEventSettings()
	local Frames = self.ConfigContainer.ConfigFrames

	if not EventSettings then
		return
	end

	assert(Frames, self.className .. " doesn't have a ConfigFrames table!")
	assert(Frames.ConfigFrames, self.className .. " isn't a JBP.C.Events_ColumnConfigContainer!")
	
	for i, frame in pairs(Frames.ConfigFrames) do
		frame:Hide()
	end

	if not desiredFrames then
		return
	end

	local lastFrame, lastFrameBottomPadding
	for i, configFrameIdentifier in ipairs(desiredFrames) do
		if not self:IsFrameBlacklisted(configFrameIdentifier) then
			local frame = Frames[configFrameIdentifier]
			
			if not frame then
				JBP:Error("Column config frame %q could not be found for event handler %q.", configFrameIdentifier, subHandlerIdentifier)
			else
				-- Data is the table passed to JBP:CInit(frame, data)
				local data = frame.data
				local yOffset = (frame.paddingTop or 0) + (lastFrameBottomPadding or 0)
				
				if lastFrame then
					frame:SetPoint("TOP", lastFrame, "BOTTOM", 0, -yOffset)
				else
					frame:SetPoint("TOP", Frames, "TOP", 0, -yOffset - 5)
				end
				frame:Show()
				lastFrame = frame

				lastFrameBottomPadding = frame.paddingBottom
			end
		end
	end	
end

JBP:NewClass("Events_ColumnConfigContainer", "Frame"){
	OnNewInstance = function(self)
		self.ConfigFrames = {}

		for i, child in JBP:Vararg(self:GetChildren()) do
			tinsert(self.ConfigFrames, child)
		end
	end,
}