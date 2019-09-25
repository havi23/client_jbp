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

JBP.SNIPPETS = {}
local SNIPPETS = JBP.SNIPPETS

SNIPPETS.Snippet_Defaults = {
	n = 0,
	["**"] = {
		Enabled = true,
		Order = 1,
		Name = L["CODESNIPPETS_DEFAULTNAME"],
		Code = "",
	}
}

JBP.Defaults.global.CodeSnippets = SNIPPETS.Snippet_Defaults
JBP.Defaults.profile.CodeSnippets = SNIPPETS.Snippet_Defaults

local RanSnippets = {}

local function RunSnippets()
	local snippets = {}
	
	for k, v in JBP:InNLengthTable(JBP.db.global.CodeSnippets) do
		snippets[#snippets + 1] = v
	end
	for k, v in JBP:InNLengthTable(JBP.db.profile.CodeSnippets) do
		snippets[#snippets + 1] = v
	end
	
	JBP:SortOrderedTables(snippets)
	
	for _, snippet in ipairs(snippets) do
		if snippet.Enabled and not SNIPPETS:HasRanSnippet(snippet) then
			SNIPPETS:RunSnippet(snippet)
		end
	end
end

function SNIPPETS:HasRanSnippet(snippet)
	return RanSnippets[snippet]
end

function SNIPPETS:RunSnippet(snippet)
	local func, err = loadstring(snippet.Code, "JBP Snippet: " .. snippet.Name)
	
	SNIPPETS.currentSnippet = snippet
	
	if func then
		func()
	elseif err then
		JBP:Error(err)
	end

	SNIPPETS.currentSnippet = nil
	
	RanSnippets[snippet] = true
end

JBP:RegisterCallback("JBP_INITIALIZE", RunSnippets)

JBP:RegisterCallback("JBP_ON_PROFILE_PRE", function(event, profileEvent, arg2, arg3)
	if profileEvent == "OnProfileChanged" then
		RunSnippets()
	end
end)


JBP:RegisterLuaImportDetector(function(table, id, parentTableName)
	if (not parentTableName or parentTableName == "CodeSnippets")
		and type(rawget(table, "Code")) == "string" and table.Code ~= "" then

		return table.Code, L["fCODESNIPPET"]:format(table.Name or L["CODESNIPPETS_DEFAULTNAME"])
	end
end)











