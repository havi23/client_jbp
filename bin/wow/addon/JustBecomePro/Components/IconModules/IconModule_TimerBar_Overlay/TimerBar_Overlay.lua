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
	

local TimerBar_Overlay = JBP:NewClass("IconModule_TimerBar_Overlay", "IconModule_TimerBar")

TimerBar_Overlay:RegisterIconDefaults{
	ShowCBar				= false,
	CBarOffs				= 0,
	InvertCBar				= false,
	Overlay_BarGCD			= false,
}

TimerBar_Overlay:RegisterConfigPanel_XMLTemplate(217, "JustBecomePro_CBarOptions")


JBP:RegisterUpgrade(60331, {
	icon = function(self, ics)
		-- Pull the setting from the profile settings, since this setting is now per-icon
		-- Also, the setting changed from "Ignore" to "Allow", so flip the boolean too.
		
		-- Old default value was true, so make sure we use true if the setting is nil from having been the same as default.
		local old = JBP.db.profile.BarGCD
		if old == nil then
			old = true
		end
		
		ics.Overlay_BarGCD = not old
	end,
})

JBP:RegisterUpgrade(51022, {
	icon = function(self, ics)
		ics.InvertCBar = not not ics.InvertBars
	end,
})


local colorSettingNames = {
	"TimerBar_StartColor",
	"TimerBar_MiddleColor",
	"TimerBar_CompleteColor",
}

function TimerBar_Overlay:SetupForIcon(sourceIcon)
	self.Invert = sourceIcon.InvertCBar
	self.Offset = sourceIcon.CBarOffs or 0
	
	self.BarGCD = sourceIcon.Overlay_BarGCD
	if sourceIcon.typeData.hasNoGCD then
		self.BarGCD = true
	end

	if not sourceIcon.typeData then
		error("sourceIcon.typeData was nil. Why did this happen? (Please tell Cybeloras)")
	end
	

	self:SetColors(
		JBP:GetColors(colorSettingNames, "TimerBar_EnableColors",
		              sourceIcon:GetSettings(), sourceIcon.group:GetSettings(), JBP.db.global)
	)
	
	self:UpdateValue(true)
end


TimerBar_Overlay:SetIconEventListner("JBP_ICON_SETUP_POST", function(Module, icon)
	if JBP.Locked then
		Module:UpdateTable_Register()
		
		Module.bar:SetAlpha(.9)
	else
		Module:UpdateTable_Unregister()
		
		Module.bar:SetValue(Module.Max)
		Module.bar:SetAlpha(.6)
		local co = Module.completeColor			
		Module.bar:SetStatusBarColor(
			co.r,
			co.g,
			co.b,
			co.a
		)
	end
end)


