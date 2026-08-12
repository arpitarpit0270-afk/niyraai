package com.niyraai.apk.voice

import android.content.Context
import android.speech.tts.TextToSpeech
import java.util.Locale

class VoiceController(context: Context) {
    private var tts: TextToSpeech? = TextToSpeech(context) { if (it == TextToSpeech.SUCCESS) tts?.language = Locale("hi", "IN") }
    fun speak(text:String) { tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "max-tts") }
    fun shutdown() { tts?.shutdown() }
}
