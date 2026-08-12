package com.niyraai.apk

import android.Manifest
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.niyraai.apk.commands.CommandRegistry
import com.niyraai.apk.conversation.AssistantViewModel

class MainActivity : ComponentActivity() {
    private val vm: AssistantViewModel by viewModels()
    private val mic = registerForActivityResult(ActivityResultContracts.RequestPermission()) {}
    override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState); setContent { App(vm, { startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)) }, { mic.launch(Manifest.permission.RECORD_AUDIO) }) } }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable fun App(vm: AssistantViewModel, openAccessibility:()->Unit, requestMic:()->Unit) {
    val s by vm.state.collectAsStateWithLifecycle()
    MaterialTheme { Scaffold(topBar={ TopAppBar(title={ Text("MAX — AI Companion") }) }) { pad -> Column(Modifier.padding(pad).padding(16.dp).verticalScroll(rememberScrollState()), verticalArrangement=Arrangement.spacedBy(12.dp)) {
        Text("MAX is an AI system, not a human. It uses Accessibility only after you grant access and follows OBSERVE → UNDERSTAND → PLAN → ACT → VERIFY → REPLAN.")
        Row(horizontalArrangement=Arrangement.spacedBy(8.dp)){ Button(openAccessibility){ Text("Enable Accessibility") }; OutlinedButton(requestMic){ Text("Enable Voice") } }
        OutlinedTextField(s.command, vm::setCommand, label={ Text("Command (Hindi, Hinglish, English)") }, modifier=Modifier.fillMaxWidth(), minLines=2)
        Button(vm::submit, Modifier.fillMaxWidth()){ Text("Ask MAX") }
        s.pendingConfirmation?.let { Card { Column(Modifier.padding(12.dp)) { Text("Confirmation required: ${it.reason}"); Row(horizontalArrangement=Arrangement.spacedBy(8.dp)){ Button(vm::confirm){ Text("Confirm") }; OutlinedButton(vm::cancel){ Text("Cancel") } } } } }
        Card { Text(s.response, Modifier.padding(16.dp)) }
        Text("Command registry: ${CommandRegistry.patterns.size} categories, ${CommandRegistry.allAliases().size} preserved aliases in-app. Add commands.txt to expand without changing safety rules.")
        Text("Debug", style=MaterialTheme.typography.titleMedium); Text(s.debug.ifBlank { "No task yet. Sensitive values are redacted from logs." })
    } } }
}
