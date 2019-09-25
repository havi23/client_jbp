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

local ldb = LibStub("LibDataBroker-1.1")
local dataobj = ldb:GetDataObjectByName("JustBecomePro") or
	ldb:NewDataObject("JustBecomePro", {
		type = "launcher",
		icon = "Interface\\Addons\\JustBecomePro\\Textures\\LDB Icon",
	})

dataobj.OnClick = function(self, button)
	if not JBP.Initialized then
		JBP:Print(L["ERROR_NOTINITIALIZED_NO_ACTION"])
		return
	end
	
	if button == "RightButton" then
		JBP:SlashCommand("options")
	else
		JBP:LockToggle()
	end
end

dataobj.OnTooltipShow = function(tt)
	tt:AddLine("JustBecomePro")
	tt:AddLine(L["LDB_TOOLTIP1"])
	tt:AddLine(L["LDB_TOOLTIP2"])
end