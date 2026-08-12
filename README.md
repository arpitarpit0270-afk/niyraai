# MAX — AI Personal Companion + Android Screen Automation Assistant

MAX is a transparent Android AI assistant prototype for Hindi, Hinglish, and English commands. It combines Jetpack Compose, a safety-first command engine, an AccessibilityService screen observer, task planning, encrypted user memory, voice/TTS hooks, and a secure-backend Gemini integration placeholder.

## Architecture

- **UI:** Jetpack Compose in `MainActivity.kt` with privacy disclosures, command entry, confirmation UI, and debug mode.
- **Observe:** `MaxAccessibilityService` captures a compressed `ScreenState` containing package/activity context and visible `Element` metadata.
- **Understand:** `NaturalLanguageEngine` handles common Hindi/Hinglish/English command families.
- **Plan:** `TaskPlanner` creates structured multi-step `TaskPlan` instances.
- **Act:** `ActionExecutor` uses official Android APIs and Accessibility actions only.
- **Verify/Replan:** Every action result returns a status and the UI exposes the loop `OBSERVE → UNDERSTAND → PLAN → ACT → VERIFY → REPLAN`.
- **Memory:** `MemoryStore` uses encrypted shared preferences and is user-controlled.
- **AI Backend:** `GeminiBackendClient` builds requests to a backend URL. Gemini API keys must never be stored in the client.

## Safety rules

MAX never claims to be human. It requests confirmation for messages, calls, payments, purchases, deleting data, security/system settings, sharing sensitive info, app installs, and permission grants. Low-confidence actions ask for clarification.

## Build

```bash
gradle :android:app:assembleDebug
```

Optional backend URL:

```bash
gradle :android:app:assembleDebug -PNIYRA_BACKEND_URL=https://your-backend.example
```
