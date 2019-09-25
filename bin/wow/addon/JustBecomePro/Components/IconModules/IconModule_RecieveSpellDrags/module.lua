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
	

local Module = JBP:NewClass("IconModule_RecieveSpellDrags", "IconModule")

Module:SetScriptHandler("OnClick", function(Module, icon, button)
	if not JBP.Locked and JBP.IE and button == "LeftButton" then
		JBP.IE:SpellItemToIcon(icon)
	end
end)

Module:SetScriptHandler("OnReceiveDrag", function(Module, icon, button)
	if not JBP.Locked and JBP.IE then
		JBP.IE:SpellItemToIcon(icon)
	end
end)


