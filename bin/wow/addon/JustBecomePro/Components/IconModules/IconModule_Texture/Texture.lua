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


	
local Texture = JBP:NewClass("IconModule_Texture", "IconModule")

Texture:RegisterAnchorableFrame("Texture")

function Texture:OnNewInstance(icon)
	self.texture = icon:CreateTexture(self:GetChildNameBase() .. "Texture", "BACKGROUND", nil, 5)
	self:SetSkinnableComponent("Icon", self.texture)
end

function Texture:OnEnable()
	local icon = self.icon
	local attributes = icon.attributes
	
	self.texture:Show()

	self:TEXTURE(icon, attributes.texture)
end
function Texture:OnDisable()
	self.texture:Hide()
end

function Texture:TEXTURE(icon, texture)
	self.texture:SetTexture(texture)
end
Texture:SetDataListener("TEXTURE")
	