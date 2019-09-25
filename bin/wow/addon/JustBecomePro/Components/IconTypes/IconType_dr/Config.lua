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

local SUG = JBP.SUG
local SpellCache = JBP:GetModule("SpellCache")

local Module = SUG:NewModule("dr", SUG:GetModule("spell"))
function Module:Table_Get()
	return SpellCache:GetCache(), JBP.BE.dr
end
function Module:Entry_Colorize_2(f, id)
	if JBP.BE.dr[id] then
		f.Background:SetVertexColor(1, .96, .41, 1) -- rogue yellow
	end
end
function Module:Entry_AddToList_2(f, id)
	if JBP.EquivFirstIDLookup[id] then -- if the entry is an equivalacy (buff, cast, or whatever)
		--NOTE: dispel types are put in JBP.EquivFirstIDLookup too for efficiency in the sorter func, but as long as dispel types are checked first, it wont matter
		local equiv = id
		local firstid = JBP.EquivFirstIDLookup[id]

		f.Name:SetText(equiv)
		f.ID:SetText(nil)

		f.insert = equiv
		f.overrideInsertName = L["SUG_INSERTEQUIV"]

		f.tooltipmethod = "JBP_SetEquiv"
		f.tooltiparg = equiv

		f.Icon:SetTexture(JBP.GetSpellTexture(firstid))
	end
end