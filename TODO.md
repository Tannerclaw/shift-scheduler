# Shift Scheduler App - TODO

**Live URL:** https://app.clawbox.us  
**Local:** http://localhost:8080  
**Location:** `/home/dan/.openclaw/workspace/shift-scheduler/`

---

## Completed ✅

- [x] **WhatsApp Integration**
  - WhatsApp button in header (📱 WhatsApp)
  - Generates formatted schedule message with date, time slots, workers
  - Opens WhatsApp with pre-filled text
  - Includes phone numbers in message

- [x] **Phone Number Support**
  - Phone field for each worker in Roster tab
  - Edit phone numbers directly
  - Auto-saves on blur

- [x] **Editable Worker Names**
  - Click name in Roster to edit
  - Auto-saves on blur

- [x] **Cloudflare Tunnel**
  - Public access via https://app.clawbox.us
  - Auto-restart via systemd service

- [x] **Local Server**
  - Running on http://localhost:8080
  - Python Flask backend

- [x] **GitHub Repository**
  - Repo: `github.com/tannerclaw/shift-scheduler`
  - Remote configured and pushed

---

## Pending ⏳

### High Priority
- [ ] **Test WhatsApp Feature**
  - Test with real crew schedule on job site
  - Verify phone numbers format correctly
  - Confirm message opens in WhatsApp properly

### Medium Priority
- [ ] **Documentation**
  - Write "how I built this" product documentation
  - Create user guide for crew foremen
  - Screenshots and feature walkthrough

- [ ] **QMD Memory Search**
  - Set up semantic search for schedule data
  - Allow searching past schedules by worker, date, project

### Low Priority / Future
- [ ] **Backup to Unraid**
  - Needs: Titan/Unraid IP and share name
  - Daily sync of schedule data

- [ ] **Multiple Workers Per Time Slot** ⚠️ REQUIRES DATA MODEL CHANGE
  - **STATUS:** Reverted to stable version — Cody's approach broke app
  - Current workaround: use 6:00 and 6:01 for two workers at same time
  - **Option B Plan:** Simpler approach — allow duplicate time entries with auto-generated unique IDs
    - Don't change existing data structure
    - Just allow same time, different slot IDs
    - Visual: show multiple pills in same slot
    - Estimated effort: 1 hour (safer than full refactor)
  - **DO NOT:** Change storage format (keep backward compatible)
  - **BACKUP:** checkpoint-20260320_133241 (stable version)

- [ ] **Additional Features**
  - Export to PDF
  - Email schedules (when email fixed)
  - Recurring schedules
  - Multiple projects/sites
  - Worker availability tracking

---

## Ideas for Later

- **Phase 1:** Shift scheduler app for concrete crews ($20-50/month)
- **Phase 2:** Content/consulting using 35 years concrete experience
- **Phase 3:** Smart concrete IoT sensors

---

*Last updated: 2026-03-20*  
*Created by: Tanner (OpenClaw assistant)*
