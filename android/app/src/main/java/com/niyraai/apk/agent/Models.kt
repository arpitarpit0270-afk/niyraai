package com.niyraai.apk.agent

import android.graphics.Rect

data class ScreenState(val packageName:String, val activityName:String?, val screenWidth:Int=0, val screenHeight:Int=0, val elements:List<Element>)
data class Element(val id:String?, val text:String?, val contentDescription:String?, val className:String?, val bounds:Rect, val clickable:Boolean, val editable:Boolean, val scrollable:Boolean, val enabled:Boolean, val visible:Boolean, val selected:Boolean)
enum class AgentAction { OPEN_APP, CLICK, TYPE, SCROLL, SWIPE, BACK, HOME, SCREEN_READ, WAIT, SELECT, CALL, MESSAGE, SEARCH, PLAY, PAUSE, STOP, SETTINGS, COMPLETE, ASK_USER, FAIL_SAFE }
enum class Confidence { HIGH, MEDIUM, LOW }
data class AgentDecision(val intent:String, val target:String?, val action:AgentAction, val confidence:Float, val reason:String, val requiresConfirmation:Boolean=false, val text:String?=null)
data class TaskStep(val action:AgentAction, val target:String?, val parameters:Map<String,String> = emptyMap(), val expectedResult:String, val retryLimit:Int=2)
data class TaskPlan(val taskId:String, val originalCommand:String, val steps:List<TaskStep>, val currentStep:Int=0, val state:String="READY")
