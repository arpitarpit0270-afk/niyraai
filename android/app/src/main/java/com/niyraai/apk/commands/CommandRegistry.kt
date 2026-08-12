package com.niyraai.apk.commands

import com.niyraai.apk.agent.AgentAction

data class CommandPattern(val category:String, val canonical:String, val aliases:List<String>, val action:AgentAction, val requiresConfirmation:Boolean=false)

object CommandRegistry {
    val patterns = listOf(
        CommandPattern("Apps", "Open app", listOf("{app} kholo", "open {app}", "{app} launch karo", "Instagram kholo", "Settings kholo"), AgentAction.OPEN_APP),
        CommandPattern("WhatsApp", "Send WhatsApp message", listOf("WhatsApp kholo aur {contact} ko message bhejo", "{contact} ko WhatsApp message bhejo", "Ali ko message bhejo"), AgentAction.MESSAGE, true),
        CommandPattern("YouTube", "Search YouTube", listOf("YouTube kholo aur {query} search karo", "funny videos search karo", "YouTube par {query} chalao"), AgentAction.SEARCH),
        CommandPattern("Navigation", "Scroll", listOf("neeche scroll karo", "scroll down", "upar scroll karo", "go back", "back jao"), AgentAction.SCROLL),
        CommandPattern("Screen", "Read screen", listOf("screen par kya hai", "screen read karo", "is page ko read karke batao", "what is on screen"), AgentAction.SCREEN_READ),
        CommandPattern("Device controls", "Settings", listOf("WiFi on karo", "Bluetooth band karo", "brightness badhao", "good night mode"), AgentAction.SETTINGS, true),
        CommandPattern("AI", "Support", listOf("mujhe motivate karo", "good night", "study mode", "friendly assistant"), AgentAction.COMPLETE)
    )
    fun allAliases(): List<String> = patterns.flatMap { it.aliases }
}
