package com.niyraai.apk.agent

import java.util.UUID

class TaskPlanner {
    fun plan(command:String, decision:AgentDecision): TaskPlan {
        val steps = when(decision.action) {
            AgentAction.MESSAGE -> listOf(TaskStep(AgentAction.OPEN_APP, "WhatsApp", expectedResult="WhatsApp opened"), TaskStep(AgentAction.TYPE, decision.target, mapOf("text" to command), "Message drafted"), TaskStep(AgentAction.MESSAGE, decision.target, expectedResult="User confirmed and message sent"))
            AgentAction.SEARCH -> listOf(TaskStep(AgentAction.OPEN_APP, "YouTube", expectedResult="YouTube opened"), TaskStep(AgentAction.SEARCH, decision.target, expectedResult="Results visible"))
            else -> listOf(TaskStep(decision.action, decision.target, expectedResult="Requested action completed"))
        }
        return TaskPlan(UUID.randomUUID().toString(), command, steps)
    }
}
