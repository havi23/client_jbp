﻿-- --------------------
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

local CNDT = JBP.CNDT


--- A [[api/conditions/api-documentation/condition-category/|ConditionCategory]] provides an interface for registering condition types.
-- 
-- It should not be directly instantiated - use CNDT:GetCategory() to get or create a category.
-- 
-- @class file
-- @name ConditionCategory.lua


local ConditionCategory = JBP:NewClass("ConditionCategory")

-- [INTERNAL] - ConditionCategories should only be constructed by CNDT:GetCategory().
function ConditionCategory:OnNewInstance(identifier, order, name, spaceBefore, spaceAfter)
	JBP:ValidateType("2 (identifier)", "ConditionCategory:New()", identifier, "string")
	JBP:ValidateType("3 (order)", "ConditionCategory:New()", order, "number")
	JBP:ValidateType("4 (name)", "ConditionCategory:New()", name, "string")
	JBP:ValidateType("5 (spaceBefore)", "ConditionCategory:New()", spaceBefore, "boolean;nil")
	JBP:ValidateType("6 (spaceAfter)", "ConditionCategory:New()", spaceAfter, "boolean;nil")
	
	self.identifier = identifier
	self.order = order
	self.name = name
	
	self.spaceBefore = spaceBefore
	self.spaceAfter = spaceAfter
	
	self.conditionData = {}

	tinsert(CNDT.Categories, self)
	JBP:SortOrderedTables(CNDT.Categories)
	
	CNDT.CategoriesByID[identifier] = self
end

--- Registers a condition to the category.
-- @param order [number] The order that the condition should be listed in its category's dropdown menu.
-- @param identifier [string] A string (all capital letters, and keep it fairly short) that will identify the condition.
-- @param conditionData [table] The data that describes the condition's appearance, function, and configuration options. See the [[api/conditions/api-documentation/condition-data-specification|Condition Data Specification]]
-- @usage 
--  ConditionCategory:RegisterCondition(1,   "SPELLCD", {
--    text = L["SPELLCOOLDOWN"],
--    range = 30,
--    step = 0.1,
--    name = function(editbox) JBP:TT(editbox, "SPELLTOCHECK", "CNDT_ONLYFIRST") editbox.label = L["SPELLTOCHECK"] end,
--    useSUG = "spellWithGCD",
--    unit = PLAYER,
--    formatter = JBP.C.Formatter.TIME_0USABLE,
--    icon = "Interface\\Icons\\spell_holy_divineintervention",
--    tcoords = CNDT.COMMON.standardtcoords,
--    funcstr = [[CooldownDuration(c.NameFirst) c.Operator c.Level]],
--    events = function(ConditionObject, c)
--      return
--        ConditionObject:GenerateNormalEventString("SPELL_UPDATE_COOLDOWN"),
--        ConditionObject:GenerateNormalEventString("SPELL_UPDATE_USABLE")
--    end,
--    anticipate = [[
--      local start, duration = GetSpellCooldown(c.GCDReplacedNameFirst)
--      local VALUE = duration and start + (duration - c.Level) or huge
--    ]],
--  })
function ConditionCategory:RegisterCondition(order, identifier, conditionData)
	JBP:ValidateType("2 (order)", "ConditionCategory:RegisterCondition()", order, "number")
	JBP:ValidateType("3 (identifier)", "ConditionCategory:RegisterCondition()", identifier, "string")
	JBP:ValidateType("4 (conditionData)", "ConditionCategory:RegisterCondition()", conditionData, "table")
	
	JBP.C.Condition:NewFromExisting(conditionData, self, order, identifier)
	
	tinsert(self.conditionData, conditionData)
	JBP:SortOrderedTables(self.conditionData)
end

--- Registers a spacer in the category's dropdown menu at the specified order (relative to other conditions)
-- @param order [number] The relative order that the spacer should be placed in.
-- @usage ConditionCategory:RegisterSpacer(10)
function ConditionCategory:RegisterSpacer(order)
	JBP:ValidateType("2 (order)", "ConditionCategory:RegisterCondition()", order, "number")
	
	local conditionData = {
		IS_SPACER = true,
		order = order
	}
	
	tinsert(self.conditionData, conditionData)
	JBP:SortOrderedTables(self.conditionData)
end