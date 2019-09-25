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

local CI = JBP.CI

local _G = _G

local pairs, tinsert, tremove = 
	  pairs, tinsert, tremove

local Type = rawget(JBP.Types, "meta")

if not Type then return end


-- GLOBALS: JustBecomePro_MetaIconOptions
-- GLOBALS: CreateFrame



Type:RegisterConfigPanel_XMLTemplate(145, "JustBecomePro_IconStates", { })

Type:RegisterConfigPanel_XMLTemplate(150, "JustBecomePro_MetaIconOptions")


Type:RegisterConfigPanel_ConstructorFunc(170, "JustBecomePro_MetaSortSettings", function(self)
	self:SetTitle(JBP.L["SORTBY"])
	self:BuildSimpleCheckSettingFrame({
		numPerRow = 3,
		function(check)
			check:SetTexts(JBP.L["SORTBYNONE"], JBP.L["SORTBYNONE_META_DESC"])
			check:SetSetting("Sort", false)
		end,
		function(check)
			check:SetTexts(JBP.L["ICONMENU_SORTASC"], JBP.L["ICONMENU_SORTASC_META_DESC"])
			check:SetSetting("Sort", -1)
		end,
		function(check)
			check:SetTexts(JBP.L["ICONMENU_SORTDESC"], JBP.L["ICONMENU_SORTDESC_META_DESC"])
			check:SetSetting("Sort", 1)
		end,
	})

	self:CScriptAdd("PanelSetup", function()
		if JBP.CI.icon:IsGroupController() then
			self:Hide()
		end
	end)
end)

JBP.IconDragger:RegisterIconDragHandler(220, -- Add to meta icon
	function(IconDragger, info)
		if IconDragger.desticon
		and IconDragger.srcicon:IsValid()
		and IconDragger.desticon.Type == "meta"
		and IconDragger.srcicon.group.viewData == IconDragger.desticon.group.viewData
		then
			info.text = L["ICONMENU_ADDMETA"]
			info.tooltipTitle = nil
			info.tooltipText = nil
			return true
		end
	end,
	function(IconDragger)
		local Icons = IconDragger.desticon:GetSettings().Icons
		if Icons[#Icons] == "" then
			Icons[#Icons] = nil
		end
		tinsert(Icons, IconDragger.srcicon:GetGUID(true))
	end
)



-- Include child icons and groups when exporting a meta icon
JBP:RegisterCallback("JBP_EXPORT_SETTINGS_REQUESTED", function(event, strings, type, settings)
	if type == "icon" and settings.Type == "meta" then
		for k, GUID in pairs(settings.Icons) do
			if GUID ~= settings.GUID then
				local type = JBP:ParseGUID(GUID)
				local settings = JBP:GetSettingsFromGUID(GUID)
				if type == "icon" and settings then
					JBP:GetSettingsStrings(strings, type, settings, JBP.Icon_Defaults)
				end
			end
		end
	end
end)



function Type:GetIconMenuText(ics)
	local text = Type.name .. " " .. L["ICONMENU_META_ICONMENUTOOLTIP"]:format(ics.Icons and #ics.Icons or 0)
	
	return text, "", true
end

function Type:GuessIconTexture(ics)
	return "Interface\\Icons\\LevelUpIcon-LFD"
end


local Config = {}
Type.Config = Config

function Config:Reload()
	JustBecomePro_MetaIconOptions:OnSettingSaved()
end

function Config:LoadConfig()
	if not JustBecomePro_MetaIconOptions then return end
	local settings = CI.ics.Icons

	for k, GUID in pairs(settings) do
		local mg = Config[k] or CreateFrame("Frame", "JustBecomePro_MetaIconOptions" .. k, JustBecomePro_MetaIconOptions, "JustBecomePro_MetaGroup", k)
		Config[k] = mg
		mg:Show()
		if k > 1 then
			mg:SetPoint("TOPLEFT", Config[k-1], "BOTTOMLEFT", 0, 0)
			mg:SetPoint("TOPRIGHT", Config[k-1], "BOTTOMRIGHT", 0, 0)
		end
		mg:SetFrameLevel(JustBecomePro_MetaIconOptions:GetFrameLevel()+2)

		mg.Icon:SetGUID(GUID)
	end

	JustBecomePro_MetaIconOptions:SetHeight((#settings * Config[1]:GetHeight()) + 35)
	
	for f=#settings+1, #Config do
		Config[f]:Hide()
	end
	Config[1]:Show()

	if settings[2] then
		Config[1].Delete:Show()
	else
		Config[1].Delete:Hide()
	end
end


---------- Click Handlers ----------
function Config:Delete(self)
	tremove(CI.ics.Icons, self:GetParent():GetID())
	Config:Reload()
end

function Config:SwapIcons(id1, id2)
	local Icons = CI.ics.Icons
	
	Icons[id1], Icons[id2] = Icons[id2], Icons[id1]
	
	Config:LoadConfig()

	-- DO NOT CALL Config:Reload() here - it will break click and drag rearranging.
	-- Config:Reload()
end


---------- Dropdown ----------
local addedGroups = {}
function Config:IconMenu()
	if JBP.DD.MENU_LEVEL == 1 then
		local currentGroupView = JBP.CI.icon.group:GetSettings().View
		
		for group in JBP:InGroups() do
			if group:ShouldUpdateIcons() then
				local info = JBP.DD:CreateInfo()

				info.text = group:GetGroupName()

				info.value = group

				if currentGroupView ~= group:GetSettings().View then
					info.disabled = true
					info.tooltipWhileDisabled = true
					
					info.tooltipTitle = info.text
					info.tooltipText = L["META_GROUP_INVALID_VIEW_DIFFERENT"]
						:format(JBP.Views[currentGroupView].name, JBP.Views[group:GetSettings().View].name)
					info.hasArrow = false
				else
					info.hasArrow = true
				end
				
				info.func = Config.IconMenuOnClick
				info.arg1 = self
				info.checked = CI.ics.Icons[self:GetParent():GetID()] == group:GetGUID()

				JBP.DD:AddButton(info)
			end
		end
	elseif JBP.DD.MENU_LEVEL == 2 then
		for icon in JBP.DD.MENU_VALUE:InIcons() do
			if icon:IsValid() and CI.icon ~= icon then
				local info = JBP.DD:CreateInfo()

				local text, textshort, tooltip = icon:GetIconMenuText()
				info.text = textshort
				info.tooltipTitle = text
				info.tooltipText = tooltip

				info.value = icon
				info.func = Config.IconMenuOnClick
				info.arg1 = self
				info.checked = CI.ics.Icons[self:GetParent():GetID()] == icon:GetGUID()

				info.tCoordLeft = 0.07
				info.tCoordRight = 0.93
				info.tCoordTop = 0.07
				info.tCoordBottom = 0.93
				info.icon = icon.attributes.texture
				JBP.DD:AddButton(info)
			end
		end
	end
end

function Config:IconMenuOnClick(frame)
	local GUID = self.value:GetGUID(true)

	assert(GUID)

	CI.ics.Icons[frame:GetParent():GetID()] = GUID

	Config:Reload()
	JBP.DD:CloseDropDownMenus()
end

