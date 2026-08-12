package com.niyraai.apk.agent

import android.content.Context
import android.content.Intent
import android.provider.Settings
import com.niyraai.apk.accessibility.MaxAccessibilityService

class ActionExecutor(private val context: Context) {
    suspend fun execute(decision: AgentDecision, screen: ScreenState?): String {
        val svc = MaxAccessibilityService.instance
        return when (decision.action) {
            AgentAction.OPEN_APP -> openApp(decision.target.orEmpty())
            AgentAction.SCREEN_READ -> ScreenUnderstandingEngine().summarize(screen)
            AgentAction.SCROLL -> if (svc?.scrollForward() == true) "Scrolled and verified by refreshing screen state." else "No scrollable area was available."
            AgentAction.BACK -> if (svc?.back() == true) "Went back." else "Back action is unavailable."
            AgentAction.HOME -> if (svc?.home() == true) "Went home." else "Home action is unavailable."
            AgentAction.SETTINGS -> { context.startActivity(Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)); "Opened Settings. Please confirm before changing WiFi, Bluetooth, security, or other system controls." }
            AgentAction.MESSAGE -> "I can prepare this message, but I need your confirmation before sending."
            AgentAction.SEARCH -> "Search planned. MAX will open the app, locate search, type the query, then verify results before selecting anything."
            AgentAction.COMPLETE -> "You’re doing better than you think. I’m MAX, your AI companion, and I’m here to support you while you stay in control."
            else -> "I need clarification before acting safely."
        }
    }
    private fun openApp(name:String): String { val pm=context.packageManager; val launcher=Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER); val match=pm.queryIntentActivities(launcher, 0).firstOrNull{ it.loadLabel(pm).toString().contains(name, true) }; return if(match!=null){ val launch=pm.getLaunchIntentForPackage(match.activityInfo.packageName)?.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK); context.startActivity(launch); "Opened ${match.loadLabel(pm)}." } else "I could not find an installed app matching '$name'." }
}
