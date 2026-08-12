package com.niyraai.apk.agent

class ScreenUnderstandingEngine {
    fun summarize(state: ScreenState?): String = if (state == null) "MAX cannot observe the screen yet. Please enable Accessibility access." else buildString {
        append("You are in ${state.packageName}. ")
        val visible = state.elements.filter { it.visible && (!it.text.isNullOrBlank() || !it.contentDescription.isNullOrBlank()) }.take(8)
        if (visible.isEmpty()) append("No readable controls were exposed by accessibility.") else append("Visible items include: ").append(visible.joinToString { it.text ?: it.contentDescription.orEmpty() })
    }
    fun findByText(state: ScreenState?, target:String): List<Element> = state?.elements.orEmpty().filter { (it.text?.contains(target, true) == true) || (it.contentDescription?.contains(target, true) == true) }
}
