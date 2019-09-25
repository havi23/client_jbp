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

local LMB = LibStub("Masque", true) or (LibMasque and LibMasque("Button"))
local type = type
local bitband = bit.band

local OnGCD = JBP.OnGCD

local ColorMSQ, OnlyMSQ

local Texture_Colored = JBP:NewClass("IconModule_Texture_Colored", "IconModule_Texture")

JBP:RegisterDatabaseDefaults({
	profile = {
		ColorMSQ = false,
		OnlyMSQ  = false,
	}
})

if LMB then
	Texture_Colored:RegisterConfigPanel_ConstructorFunc(9, "JustBecomePro_Main_Texture_Colored", function(self)
		self:SetTitle(L["DOMAIN_PROFILE"] .. ": " .. "Masque")
		
		self:BuildSimpleCheckSettingFrame({
			numPerRow = 1,
			function(check)
				check:SetTexts(L["COLOR_MSQ_COLOR"], L["COLOR_MSQ_COLOR_DESC"])
				check:SetSetting("ColorMSQ")
			end,
			function(check)
				check:SetTexts(L["COLOR_MSQ_ONLY"], L["COLOR_MSQ_ONLY_DESC"])
				check:SetSetting("OnlyMSQ")

				check:CScriptAdd("ReloadRequested", function()
					check:SetEnabled(JBP.db.profile.ColorMSQ)
				end)
			end,
		})
	end):SetPanelSet("profile")
end


function Texture_Colored:SetupForIcon(icon)
	self.ShowTimer = icon.ShowTimer
	self:STATE(icon, icon.attributes.calculatedState)
end

function Texture_Colored:VarTexChanged()
	local icon = self.icon
	self:STATE(icon, icon.attributes.calculatedState)
end

local COLOR_UNLOCKED = {
	Color = "ffffffff",
	Texture = "",
	Gray = false,
}
function Texture_Colored:STATE(icon, stateData)
	local color
	if not JBP.Locked or not stateData then
		color = "ffffffff"
	else
		color = stateData.Color or "ffffffff"
	end

	local texture = stateData.Texture
	if texture and texture ~= "" then
		texture = JBP.COMMON.Textures:EvaluateTexturePath(texture, self, "VarTexChanged")
		self.texture:SetTexture(texture)
	else
		self.texture:SetTexture(icon.attributes.texture)
	end
	
	local c = JBP:StringToCachedRGBATable(color)
	
	if not (LMB and OnlyMSQ) then
		self.texture:SetVertexColor(c.r, c.g, c.b, 1)
	else
		self.texture:SetVertexColor(1, 1, 1, 1)
	end

	self.texture:SetDesaturated(c.flags and c.flags.desaturate or false)
	
	if LMB and ColorMSQ then
		-- This gets set by IconModule_IconContainer_Masque
		local normaltex = icon.normaltex
		if normaltex then
			normaltex:SetVertexColor(c.r, c.g, c.b, 1)
		end
	end
end

Texture_Colored:SetDataListener("CALCULATEDSTATE", Texture_Colored.STATE)


function Texture_Colored:TEXTURE(icon, texture)
	self:STATE(icon, icon.attributes.calculatedState)
end
Texture_Colored:SetDataListener("TEXTURE")

JBP:RegisterCallback("JBP_GLOBAL_UPDATE", function()
	ColorMSQ = JBP.db.profile.ColorMSQ
	OnlyMSQ = JBP.db.profile.OnlyMSQ
end)