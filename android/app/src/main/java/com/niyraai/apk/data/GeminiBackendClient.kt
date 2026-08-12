package com.niyraai.apk.data

import com.niyraai.apk.BuildConfig
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody

class GeminiBackendClient(private val client: OkHttpClient = OkHttpClient()) {
    fun endpoint() = BuildConfig.NIYRA_BACKEND_URL
    fun buildRequest(path:String, json:String): Request = Request.Builder().url(endpoint().trimEnd('/') + path).post(json.toRequestBody("application/json".toMediaType())).build()
}
