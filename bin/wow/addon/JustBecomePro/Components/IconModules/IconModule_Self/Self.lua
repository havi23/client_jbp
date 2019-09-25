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

-- The point of this module is to expose the icon itself to the
-- anchorable frames list.
	
local Module = JBP:NewClass("IconModule_Self", "IconModule")
Module:SetAllowanceForType("", false)

Module:RegisterAnchorableFrame("Icon")

function Module:OnNewInstance(icon)
	_G[self:GetChildNameBase() .. "Icon"] = icon
end