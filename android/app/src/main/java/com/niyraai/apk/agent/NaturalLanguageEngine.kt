package com.niyraai.apk.agent

class NaturalLanguageEngine {
    fun decide(command: String, screen: ScreenState?): AgentDecision {
        val c = command.lowercase().trim()
        return when {
            listOf("screen", "page", "kya hai", "read").any { c.contains(it) } -> AgentDecision("screen_read", null, AgentAction.SCREEN_READ, .92f, "User asked to summarize visible screen")
            c.contains("whatsapp") || c.contains("message") -> AgentDecision("message", extractAfter(command, "ko"), AgentAction.MESSAGE, .72f, "Messaging is sensitive", requiresConfirmation = true, text = command)
            c.contains("youtube") || c.contains("search") -> AgentDecision("search", command.substringAfter("search", command), AgentAction.SEARCH, .82f, "Search request detected")
            c.contains("scroll") || c.contains("neeche") -> AgentDecision("scroll", "down", AgentAction.SCROLL, .9f, "Navigation command")
            c.contains("back") || c.contains("wapas") -> AgentDecision("back", null, AgentAction.BACK, .9f, "Back navigation")
            c.contains("wifi") || c.contains("bluetooth") || c.contains("settings") -> AgentDecision("settings", command, AgentAction.SETTINGS, .76f, "System setting change needs confirmation", true)
            c.contains("open") || c.contains("kholo") -> AgentDecision("open_app", command.replace("kholo", "").replace("open", "").trim(), AgentAction.OPEN_APP, .86f, "Open app command")
            c.contains("motivate") -> AgentDecision("support", null, AgentAction.COMPLETE, .95f, "Motivational support")
            else -> AgentDecision("unknown", null, AgentAction.ASK_USER, .25f, "Command is ambiguous")
        }
    }
    private fun extractAfter(s:String, token:String)=s.substringBefore(token, "").trim().ifBlank { null }
}
