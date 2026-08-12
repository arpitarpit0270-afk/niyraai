package com.niyraai.apk.data

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class MemoryStore(context: Context) {
    private val prefs = EncryptedSharedPreferences.create(context, "max_memory", MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(), EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV, EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM)
    fun savePreference(key:String, value:String) = prefs.edit().putString(key, value).apply()
    fun readPreference(key:String): String? = prefs.getString(key, null)
    fun clear() = prefs.edit().clear().apply()
}
