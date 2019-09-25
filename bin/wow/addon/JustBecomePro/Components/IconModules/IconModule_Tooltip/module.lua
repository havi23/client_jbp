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
	

local Module = JBP:NewClass("IconModule_Tooltip", "IconModule")
local title_default = function(icon)
	
	local line1 = "JustBecomePro " .. icon:GetIconName()
	
	return line1
end
Module.title = title_default

local text_default = L["ICON_TOOLTIP2NEW"]
Module.text = text_default

Module:PostHookMethod("OnUnimplementFromIcon", function(self)
	self:SetTooltipTitle(title_default, true)
	self:SetTooltipText(text_default, true)
end)

function Module:OnDisable()
	if self.icon:IsMouseOver() and self.icon:IsVisible() then
		GameTooltip:Hide()
	end
end

function Module:SetTooltipTitle(title, dontUpdate)
	self.title = title
	
	-- this should work, even though this tooltip isn't manged by JBP's tooltip handler
	-- (TT_Update is really generic)
	if not dontUpdate then
		JBP:TT_Update(self.icon)
	end
end
function Module:SetTooltipText(text, dontUpdate)
	self.text = text
	
	-- this should work, even though this tooltip isn't manged by JBP's tooltip handler
	-- (TT_Update is really generic)
	if not dontUpdate then
		JBP:TT_Update(self.icon)
	end
end

Module:SetScriptHandler("OnEnter", function(Module, icon)
	if not JBP.Locked then
		JBP:TT_Anchor(icon)
		GameTooltip:AddLine(JBP.get(Module.title, icon), HIGHLIGHT_FONT_COLOR.r, HIGHLIGHT_FONT_COLOR.g, HIGHLIGHT_FONT_COLOR.b, false)
		
			
		local GroupPosition = icon.group:GetModuleOrModuleChild("GroupModule_GroupPosition")
		if GroupPosition and not GroupPosition:CanMove() then
			GameTooltip:AddLine(L["LOCKED2"], NORMAL_FONT_COLOR.r, NORMAL_FONT_COLOR.g, NORMAL_FONT_COLOR.b, true)
		end
		
		if icon:IsControlled() then
			GameTooltip:AddLine(L["ICON_TOOLTIP_CONTROLLED"], NORMAL_FONT_COLOR.r, NORMAL_FONT_COLOR.g, NORMAL_FONT_COLOR.b, true)
		else
			GameTooltip:AddLine(JBP.get(Module.text, icon), NORMAL_FONT_COLOR.r, NORMAL_FONT_COLOR.g, NORMAL_FONT_COLOR.b, false)
		end

		local currentFocus = GetCurrentKeyBoardFocus()
		if currentFocus and currentFocus.GetAcceptsJBPLinks then
			local accepts, linkDesc = currentFocus:GetAcceptsJBPLinks()
			if accepts then
				GameTooltip:AddLine(" ")
				GameTooltip:AddLine(linkDesc, NORMAL_FONT_COLOR.r, NORMAL_FONT_COLOR.g, NORMAL_FONT_COLOR.b, false)
			end
		end

		if icon:IsGroupController() then
			GameTooltip:AddLine(" ")
			GameTooltip:AddLine(L["ICON_TOOLTIP_CONTROLLER"], NORMAL_FONT_COLOR.r, NORMAL_FONT_COLOR.g, NORMAL_FONT_COLOR.b, false)
		end

		if JBP.db.global.ShowGUIDs then
			GameTooltip:AddLine(" ")
			if not icon.TempGUID then
				GameTooltip:AddLine(icon:GetGUID(), HIGHLIGHT_FONT_COLOR.r, HIGHLIGHT_FONT_COLOR.g, HIGHLIGHT_FONT_COLOR.b, false)
			end
			GameTooltip:AddLine(icon.group:GetGUID(), HIGHLIGHT_FONT_COLOR.r, HIGHLIGHT_FONT_COLOR.g, HIGHLIGHT_FONT_COLOR.b, false)
		end

		GameTooltip:Show()
	end
end)

Module:SetScriptHandler("OnLeave", function(Module, icon)
	GameTooltip:Hide()
end)



