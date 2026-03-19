import logging
import json
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot token
TOKEN = "8692194133:AAG9jUBOkXOtKdRczKvxIi3oL1mcJDp4CNg"

# Server API
API_URL = "http://localhost:8080/api/data"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def get_schedule_data():
    """Fetch schedule from server"""
    try:
        response = requests.get(API_URL, timeout=5)
        return response.json()
    except:
        return None

def format_time(t):
    """Convert 24h to 12h format"""
    h, m = map(int, t.split(':'))
    ap = 'AM' if h < 12 else 'PM'
    h = h % 12 or 12
    return f"{h}:{m:02d}{ap.lower()}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await update.message.reply_text(
        "🗓️ *Shift Scheduler Bot*\n\n"
        "Commands:\n"
        "/schedule - View today's schedule\n"
        "/workers - List all workers\n"
        "/roster - Who's working today\n"
        "/send - Send schedule via WhatsApp\n\n"
        "Need help? Ask your supervisor!",
        parse_mode='Markdown'
    )

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show schedule"""
    data = await get_schedule_data()
    if not data:
        await update.message.reply_text("❌ Can't connect to server. Try again later.")
        return
    
    workers = data.get('workers', [])
    slots = data.get('slots', [])
    assignments = data.get('assignments', {})
    
    if not slots:
        await update.message.reply_text("📭 No time slots set up yet.")
        return
    
    msg = "*Start Times*\n\n"
    has_workers = False
    
    for slot in slots:
        time = slot['time']
        assigned = assignments.get(time, [])
        available = [w for w in assigned if not workers.get(w, {}).get('unavailable', False)]
        
        if available:
            has_workers = True
            msg += f"*{format_time(time)}*\n"
            for name in available:
                msg += f"• {name}\n"
            msg += "\n"
    
    if not has_workers:
        msg += "No one assigned yet.\n\n"
    
    # Off work
    off_work = [w['name'] for w in workers if not w.get('unavailable') and w['name'] not in [n for a in assignments.values() for n in a]]
    if off_work:
        msg += "*Off Work*\n"
        for name in off_work[:10]:
            msg += f"• {name}\n"
        if len(off_work) > 10:
            msg += f"...and {len(off_work) - 10} more\n"
    
    total = len(workers)
    on_shift = sum(len([n for n in a if n in [w['name'] for w in workers]]) for a in assignments.values())
    
    msg += f"\nTotal: {total} | On: {on_shift}"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def workers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all workers"""
    data = await get_schedule_data()
    if not data:
        await update.message.reply_text("❌ Can't connect to server.")
        return
    
    workers = data.get('workers', [])
    if not workers:
        await update.message.reply_text("👥 No workers in roster.")
        return
    
    msg = "*All Workers*\n\n"
    for w in workers:
        status = "🟢" if not w.get('unavailable') else "🔴"
        msg += f"{status} {w['name']}"
        if w.get('phone'):
            msg += f" 📞 {w['phone']}"
        msg += "\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def roster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick roster check"""
    data = await get_schedule_data()
    if not data:
        await update.message.reply_text("❌ Can't connect to server.")
        return
    
    workers = data.get('workers', [])
    assignments = data.get('assignments', {})
    
    on_shift = []
    for slot, names in assignments.items():
        for name in names:
            w = next((x for x in workers if x['name'] == name), None)
            if w and not w.get('unavailable'):
                on_shift.append((name, slot))
    
    off_work = [w['name'] for w in workers if not w.get('unavailable') and w['name'] not in [n for n, _ in on_shift]]
    out_sick = [w['name'] for w in workers if w.get('unavailable')]
    
    msg = "*Today's Roster*\n\n"
    
    if on_shift:
        msg += f"🟢 *On Shift ({len(on_shift)})*\n"
        for name, slot in on_shift[:15]:
            msg += f"• {name} - {format_time(slot)}\n"
        if len(on_shift) > 15:
            msg += f"...and {len(on_shift) - 15} more\n"
        msg += "\n"
    
    if off_work:
        msg += f"⚪ *Off/Not Assigned ({len(off_work)})*\n"
        for name in off_work[:10]:
            msg += f"• {name}\n"
        if len(off_work) > 10:
            msg += f"...and {len(off_work) - 10} more\n"
        msg += "\n"
    
    if out_sick:
        msg += f"🔴 *Out/Sick ({len(out_sick)})*\n"
        for name in out_sick:
            msg += f"• {name}\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send schedule via WhatsApp"""
    keyboard = [[InlineKeyboardButton("📱 Generate WhatsApp Message", callback_data='generate_whatsapp')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Click below to generate a WhatsApp message with today's schedule.",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'generate_whatsapp':
        data = await get_schedule_data()
        if not data:
            await query.edit_message_text("❌ Can't connect to server.")
            return
        
        workers = data.get('workers', [])
        slots = data.get('slots', [])
        assignments = data.get('assignments', {})
        
        import datetime
        date = datetime.datetime.now().strftime("%A, %B %d")
        
        msg = f"*Start Times*{date}%0A%0A"
        
        for slot in slots:
            time = slot['time']
            assigned = assignments.get(time, [])
            available = [w for w in assigned if w not in [x['name'] for x in workers if x.get('unavailable')]]
            
            if available:
                msg += f"{format_time(time).replace(' ', '').lower()}%0A"
                for name in available:
                    msg += f"{name}%0A"
                msg += "%0A"
        
        off_work = [w['name'] for w in workers if not w.get('unavailable') and w['name'] not in [n for a in assignments.values() for n in a]]
        if off_work:
            msg += "*Off Work*%0A"
            for name in off_work:
                msg += f"{name}%0A"
            msg += "%0A"
        
        total = len(workers)
        on_shift = sum(len([n for n in a if n in [w['name'] for w in workers]]) for a in assignments.values())
        out = len([w for w in workers if w.get('unavailable')])
        off = total - on_shift - out
        
        msg += f"Total: {total} On: {on_shift}"
        if out:
            msg += f" Out: {out}"
        if off:
            msg += f" Off: {off}"
        
        whatsapp_url = f"https://wa.me/?text={msg}"
        
        await query.edit_message_text(
            f"✅ Schedule generated!\n\n"
            f"[Click here to open WhatsApp]({whatsapp_url})",
            parse_mode='Markdown'
        )

def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", schedule))
    application.add_handler(CommandHandler("workers", workers))
    application.add_handler(CommandHandler("roster", roster))
    application.add_handler(CommandHandler("send", send))
    
    # Callbacks
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start
    application.run_polling()

if __name__ == "__main__":
    main()
