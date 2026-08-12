package com.niyraai.apk.accessibility

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.AccessibilityServiceInfo
import android.graphics.Rect
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.niyraai.apk.agent.Element
import com.niyraai.apk.agent.ScreenState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class MaxAccessibilityService : AccessibilityService() {
    override fun onServiceConnected() { instance = this; serviceInfo = serviceInfo.apply { flags = flags or AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS } }
    override fun onAccessibilityEvent(event: AccessibilityEvent?) { mutableLatest.value = capture() }
    override fun onInterrupt() {}
    fun capture(): ScreenState? {
        val root = rootInActiveWindow ?: return null
        val out = mutableListOf<Element>(); walk(root, out)
        return ScreenState(root.packageName?.toString().orEmpty(), root.viewIdResourceName, elements = out)
    }
    fun click(element: Element): Boolean = findNode(rootInActiveWindow, element)?.performAction(AccessibilityNodeInfo.ACTION_CLICK) == true
    fun scrollForward(): Boolean = findScrollable(rootInActiveWindow)?.performAction(AccessibilityNodeInfo.ACTION_SCROLL_FORWARD) == true
    fun back(): Boolean = performGlobalAction(GLOBAL_ACTION_BACK)
    fun home(): Boolean = performGlobalAction(GLOBAL_ACTION_HOME)
    private fun walk(node: AccessibilityNodeInfo?, out: MutableList<Element>) { if (node == null) return; val r=Rect(); node.getBoundsInScreen(r); out += Element(node.viewIdResourceName,node.text?.toString(),node.contentDescription?.toString(),node.className?.toString(),r,node.isClickable,node.isEditable,node.isScrollable,node.isEnabled,node.isVisibleToUser,node.isSelected); repeat(node.childCount){ walk(node.getChild(it), out) } }
    private fun findScrollable(n: AccessibilityNodeInfo?): AccessibilityNodeInfo? { if (n == null) return null; if (n.isScrollable) return n; repeat(n.childCount){ findScrollable(n.getChild(it))?.let { return it } }; return null }
    private fun findNode(n: AccessibilityNodeInfo?, e: Element): AccessibilityNodeInfo? { if (n == null) return null; val r=Rect(); n.getBoundsInScreen(r); if (r == e.bounds && n.text?.toString()==e.text) return n; repeat(n.childCount){ findNode(n.getChild(it), e)?.let { return it } }; return null }
    companion object { var instance: MaxAccessibilityService? = null; private val mutableLatest = MutableStateFlow<ScreenState?>(null); val latest: StateFlow<ScreenState?> = mutableLatest }
}
