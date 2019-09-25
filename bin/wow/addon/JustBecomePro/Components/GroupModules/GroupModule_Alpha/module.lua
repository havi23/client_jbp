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


local GroupModule_Alpha = JBP:NewClass("GroupModule_Alpha", "GroupModule"){	
	OnEnable = function(self)
		local group = self.group
		if JBP.Locked then
			group:SetAlpha(group:GetSettings().Alpha)
		else
			self:Disable()
		end
	end,
	
	OnDisable = function(self)
		self.group:SetAlpha(1)
	end,
}

GroupModule_Alpha:RegisterConfigPanel_XMLTemplate(35, "JustBecomePro_GM_Alpha")

GroupModule_Alpha:RegisterGroupDefaults{
	Alpha = 1,
}
