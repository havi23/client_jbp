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


JBP.CONST.STATE.DEFAULT_STACKSFAILED = 101
local STATE = JBP.CONST.STATE.DEFAULT_STACKSFAILED

local floor = floor

local Hook = JBP.Classes.IconDataProcessorHook:New("STATE_STACKREQ", "STACK")

Hook:RegisterConfigPanel_XMLTemplate(225, "JustBecomePro_StackRequirements")

Hook:RegisterIconDefaults{
	StackMin				= 0,
	StackMax				= 0,
	StackMinEnabled			= false,
	StackMaxEnabled			= false,
}

JBP:RegisterUpgrade(80013, {
	icon = function(self, ics)
		ics.States[STATE].Alpha = ics.StackAlpha or 0
		ics.StackAlpha = nil
	end,
})
JBP:RegisterUpgrade(60000, {
	icon = function(self, ics)
		ics.StackMin = floor(tonumber(ics.StackMin)) or 0
		ics.StackMax = floor(tonumber(ics.StackMax)) or 0
	end,
})
JBP:RegisterUpgrade(23000, {
	icon = function(self, ics)
		if ics.StackMin ~= JBP.Icon_Defaults.StackMin then
			ics.StackMinEnabled = true
		end
		if ics.StackMax ~= JBP.Icon_Defaults.StackMax then
			ics.StackMaxEnabled = true
		end
	end,
})
JBP:RegisterUpgrade(60010, {
	icon = function(self, ics)
		ics.StackAlpha = ics.ConditionAlpha
	end,
})



-- Create an IconDataProcessor that will store the result of the stack test
local Processor = JBP.Classes.IconDataProcessor:New("STATE_STACKSFAILED", "state_stackFailed")
Processor.dontInherit = true
Processor:RegisterAsStateArbitrator(30, Hook, false, function(icon)
	local ics = icon:GetSettings()
	if not ics.StackMinEnabled and not ics.StackMaxEnabled then
		return nil
	end

	local text = ""
	if ics.StackMinEnabled then
		text = L["STACKS"] .. " < " .. ics.StackMin
	end
	if ics.StackMaxEnabled then
		if ics.StackMinEnabled then
			text = text .. " " .. L["CONDITIONPANEL_OR"]:lower() .. " "
		end
		text = text .. L["STACKS"] .. " > " .. ics.StackMax
	end
	
	return {
		[STATE] = { text = text, tooltipText = L["STACKALPHA_DESC"]},
	}
end)

Hook:DeclareUpValue("STATE_DEFAULT_STACKSFAILED",  STATE)
Hook:RegisterCompileFunctionSegmentHook("post", function(Processor, t)
	-- GLOBALS: stack
	t[#t+1] = [[
	
	local state_stackFailed = nil
	if
		stack and ((icon.StackMinEnabled and icon.StackMin > stack) or (icon.StackMaxEnabled and stack > icon.StackMax))
	then
		state_stackFailed = icon.States[STATE_DEFAULT_STACKSFAILED]
	end
	
	if attributes.state_stackFailed ~= state_stackFailed then
		icon:SetInfo_INTERNAL("state_stackFailed", state_stackFailed)
		doFireIconUpdated = true
	end
	--]]
end)