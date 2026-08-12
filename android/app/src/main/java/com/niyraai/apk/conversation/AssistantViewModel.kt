package com.niyraai.apk.conversation

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.niyraai.apk.accessibility.MaxAccessibilityService
import com.niyraai.apk.agent.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class AssistantUiState(val command:String="", val response:String="Hi, I’m MAX — a transparent AI assistant. Enable Accessibility to let me observe and act with your control.", val pendingConfirmation: AgentDecision?=null, val debug:String="")

class AssistantViewModel(app: Application): AndroidViewModel(app) {
    private val nlu = NaturalLanguageEngine(); private val planner = TaskPlanner(); private val executor = ActionExecutor(app)
    private val _state = MutableStateFlow(AssistantUiState()); val state: StateFlow<AssistantUiState> = _state
    fun setCommand(v:String){ _state.value = _state.value.copy(command=v) }
    fun submit(){ val command=_state.value.command; val screen=MaxAccessibilityService.latest.value; val decision=nlu.decide(command, screen); val plan=planner.plan(command, decision); if(decision.requiresConfirmation || decision.confidence in .45f.. .79f){ _state.value=_state.value.copy(response="Before I act: ${decision.reason}. Confirm?", pendingConfirmation=decision, debug=plan.toString()); return }; run(decision, screen, plan) }
    fun confirm(){ val d=_state.value.pendingConfirmation ?: return; run(d, MaxAccessibilityService.latest.value, planner.plan(_state.value.command, d)) }
    fun cancel(){ _state.value=_state.value.copy(response="Cancelled. I will not act without your approval.", pendingConfirmation=null) }
    private fun run(decision:AgentDecision, screen:ScreenState?, plan:TaskPlan){ viewModelScope.launch { val result=executor.execute(decision, screen); _state.value=_state.value.copy(response=result, pendingConfirmation=null, debug="OBSERVE → UNDERSTAND → PLAN → ACT → VERIFY → REPLAN\n$plan") } }
}
