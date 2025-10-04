import os
import logging
import httpx
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = os.getenv("TELEGRAM_ALLOWED_USER_IDS", "").split(",")
ALLOWED_USER_IDS = [int(uid.strip()) for uid in ALLOWED_USER_IDS if uid.strip()]

# Vendor keyboard
VENDOR_KEYBOARD = [
    [
        InlineKeyboardButton("OpenAI", callback_data="vendor:openai"),
        InlineKeyboardButton("Claude", callback_data="vendor:claude")
    ],
    [
        InlineKeyboardButton("Grok", callback_data="vendor:grok"),
        InlineKeyboardButton("Gemini", callback_data="vendor:gemini")
    ],
    [
        InlineKeyboardButton("Qwen", callback_data="vendor:qwen"),
        InlineKeyboardButton("DeepSeek", callback_data="vendor:deepseek")
    ],
    [
        InlineKeyboardButton("🧠 Think Mode (Personalized)", callback_data="think_mode")
    ]
]

# Think Mode question selection keyboard
THINK_MODE_KEYBOARD = [
    [
        InlineKeyboardButton("5 Questions", callback_data="think:5"),
        InlineKeyboardButton("10 Questions", callback_data="think:10"),
        InlineKeyboardButton("25 Questions", callback_data="think:25")
    ]
]

# Conversation states for Think Mode
ANSWERING_QUESTIONS = 1


def check_access(user_id: int) -> bool:
    """Check if user has access to the bot."""
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.effective_user.id

    if not check_access(user_id):
        await update.message.reply_text("Access denied. You are not authorized to use this bot.")
        return

    welcome_message = """
🤖 <b>Local LLM Prompt Optimizer Bot</b>

I help you optimize prompts for different LLM vendors!

<b>How to use:</b>
1. Send me any prompt text
2. Choose your target vendor (OpenAI, Claude, Grok, etc.)
3. Get an optimized prompt with vendor-specific enhancements

<b>Commands:</b>
/start - Show this message
/help - Get help
/optimize - Start optimization process

<b>Credits:</b>
Created by Danil Silantyev (@Danil_Silantyev)
<a href="https://t.me/DevsOpenNetwork">NDDev OpenNetwork</a> | <a href="https://nddev.tech">nddev.tech</a>
"""
    await update.message.reply_text(welcome_message, parse_mode='HTML', disable_web_page_preview=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
<b>How to optimize prompts:</b>

1. Send me your prompt text directly, or use /optimize
2. I'll ask you to choose the target LLM vendor
3. You'll receive an optimized version with:
   - Vendor-specific formatting
   - Enhanced structure
   - Optimization notes
   - Usage recommendations

<b>Supported vendors:</b>
• OpenAI (GPT-4o, o1, o3-mini, o4-mini)
• Claude (Claude 3.7 Sonnet, Claude 3.5 Haiku)
• Grok (Grok 4, Grok 4 Fast, Grok Code Fast 1)
• Gemini (Gemini 2.5 Pro, Gemini 2.5 Flash)
• Qwen (Qwen3-235B, Qwen3-30B, QwQ-32B)
• DeepSeek (DeepSeek V3.2-Exp, DeepSeek R1-0528)

Each vendor has unique optimization strategies!

<b>Community:</b>
Join <a href="https://t.me/DevsOpenNetwork">NDDev OpenNetwork</a> for updates and support
"""
    await update.message.reply_text(help_text, parse_mode='HTML', disable_web_page_preview=True)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages."""
    user_id = update.effective_user.id

    if not check_access(user_id):
        await update.message.reply_text("Access denied.")
        return

    # Store the prompt in context
    context.user_data['prompt'] = update.message.text

    # Show vendor selection
    reply_markup = InlineKeyboardMarkup(VENDOR_KEYBOARD)
    await update.message.reply_text(
        "Choose the target LLM vendor:",
        reply_markup=reply_markup
    )


async def vendor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle vendor selection callback."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    if not check_access(user_id):
        await query.message.reply_text("Access denied.")
        return

    # Extract vendor from callback data
    vendor_str = query.data.split(":")[1]

    # Get stored prompt
    prompt = context.user_data.get('prompt')
    if not prompt:
        await query.message.reply_text("No prompt found. Please send a prompt first.")
        return

    # Show processing message
    await query.edit_message_text(f"Optimizing for {vendor_str}... ⏳")

    try:
        # Call API to optimize
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/api/optimize",
                json={
                    "prompt": prompt,
                    "vendor": vendor_str
                }
            )
            response.raise_for_status()
            result = response.json()

        # Create clean prompt file - just the prompt, nothing else
        file_content = result['optimized']

        # Send as file
        file_buffer = BytesIO(file_content.encode('utf-8'))
        file_buffer.name = f"optimized_prompt_{result['vendor']}.txt"

        # Send info message with recommendations
        info_message = f"""✅ <b>Optimization Complete!</b>

<b>Vendor:</b> {result['vendor'].upper()}
<b>Format:</b> {result['metadata'].get('format', 'N/A')}
<b>Recommended Model:</b> {result['metadata'].get('model_recommendation', 'N/A')}
<b>Temperature:</b> {result['metadata'].get('temperature_recommendation', 'N/A')}

<b>Enhancement Notes:</b>
{result['enhancement_notes']}

📎 Clean prompt attached - ready to copy & paste!"""

        await query.message.reply_text(info_message, parse_mode='HTML')
        await query.message.reply_document(
            document=file_buffer,
            filename=f"optimized_prompt_{result['vendor']}.txt"
        )

        # Send credits as separate message
        credits = """🤖 Prompt optimized by <b>Local LLM Prompt Optimizer</b>

👨‍💻 Created by <a href="https://t.me/Danil_Silantyev">Danil Silantyev</a>
🌐 <a href="https://t.me/DevsOpenNetwork">DevsOpenNetwork</a>"""

        await query.message.reply_text(credits, parse_mode='HTML', disable_web_page_preview=True)

    except httpx.HTTPError as e:
        logger.error(f"API error: {e}", exc_info=True)
        await query.message.reply_text(
            f"❌ Optimization failed: API error\\n\\nPlease check if backend service is running."
        )
    except Exception as e:
        logger.error(f"Optimization error: {e}", exc_info=True)
        await query.message.reply_text(
            f"❌ Optimization failed: {str(e)}"
        )


async def think_mode_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Think Mode selection."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    if not check_access(user_id):
        await query.message.reply_text("Access denied.")
        return

    # Show vendor selection for Think Mode
    vendor_keyboard_think = [
        [
            InlineKeyboardButton("OpenAI", callback_data="think_vendor:openai"),
            InlineKeyboardButton("Claude", callback_data="think_vendor:claude")
        ],
        [
            InlineKeyboardButton("Grok", callback_data="think_vendor:grok"),
            InlineKeyboardButton("Gemini", callback_data="think_vendor:gemini")
        ],
        [
            InlineKeyboardButton("Qwen", callback_data="think_vendor:qwen"),
            InlineKeyboardButton("DeepSeek", callback_data="think_vendor:deepseek")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(vendor_keyboard_think)
    await query.edit_message_text(
        "🧠 <b>Think Mode</b>\n\nChoose the target LLM vendor:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def think_vendor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle vendor selection in Think Mode."""
    query = update.callback_query
    await query.answer()

    # Extract vendor
    vendor = query.data.split(":")[1]
    context.user_data['think_vendor'] = vendor

    # Show question number selection
    reply_markup = InlineKeyboardMarkup(THINK_MODE_KEYBOARD)
    await query.edit_message_text(
        f"🧠 <b>Think Mode - {vendor.upper()}</b>\n\nHow many clarifying questions would you like to answer?",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def think_num_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle question number selection."""
    query = update.callback_query
    await query.answer()

    num_questions = int(query.data.split(":")[1])
    vendor = context.user_data.get('think_vendor')
    prompt = context.user_data.get('prompt')

    if not prompt or not vendor:
        await query.message.reply_text("Error: Missing prompt or vendor. Please start over.")
        return ConversationHandler.END

    # Show processing message
    await query.edit_message_text(f"Generating {num_questions} questions... ⏳")

    try:
        # Call API to generate questions
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/api/think/generate-questions",
                json={
                    "prompt": prompt,
                    "vendor": vendor,
                    "num_questions": num_questions
                }
            )
            response.raise_for_status()
            result = response.json()

        # Store questions and initialize answers
        context.user_data['questions'] = result['questions']
        context.user_data['answers'] = []
        context.user_data['current_question_index'] = 0

        # Delete the processing message
        await query.message.delete()

        # Ask the first question
        await ask_next_question(update, context)

        return ANSWERING_QUESTIONS

    except Exception as e:
        logger.error(f"Question generation error: {e}", exc_info=True)
        await query.message.reply_text(f"❌ Failed to generate questions: {str(e)}")
        return ConversationHandler.END


async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the next question in Think Mode."""
    questions = context.user_data.get('questions', [])
    current_index = context.user_data.get('current_question_index', 0)

    if current_index < len(questions):
        question = questions[current_index]
        await update.effective_message.reply_text(
            f"🧠 <b>Question {current_index + 1} of {len(questions)}</b>\n\n{question}\n\n💬 Send your answer:",
            parse_mode='HTML'
        )
    else:
        # All questions answered, optimize with answers
        await finalize_think_mode(update, context)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user's answer to a question."""
    user_id = update.effective_user.id

    if not check_access(user_id):
        await update.message.reply_text("Access denied.")
        return ConversationHandler.END

    answer = update.message.text
    context.user_data['answers'].append(answer)
    context.user_data['current_question_index'] += 1

    await ask_next_question(update, context)

    return ANSWERING_QUESTIONS


async def finalize_think_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finalize Think Mode and optimize with answers."""
    prompt = context.user_data.get('prompt')
    vendor = context.user_data.get('think_vendor')
    questions = context.user_data.get('questions')
    answers = context.user_data.get('answers')

    # Show processing message
    processing_msg = await update.effective_message.reply_text(
        "✨ Creating your perfect personalized prompt... ⏳"
    )

    try:
        # Debug logging
        logger.info(f"Think Mode finalize - Questions: {len(questions) if questions else 0}, Answers: {len(answers) if answers else 0}")
        logger.info(f"Questions: {questions}")
        logger.info(f"Answers: {answers}")

        # Call API to optimize with answers
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/api/think/optimize-with-answers",
                json={
                    "prompt": prompt,
                    "vendor": vendor,
                    "questions": questions,
                    "answers": answers
                }
            )

            if not response.is_success:
                logger.error(f"API error response: {response.text}")

            response.raise_for_status()
            result = response.json()

        # Delete processing message
        await processing_msg.delete()

        # Send optimized result (same format as regular optimization)
        await send_optimized_prompt(update, result)

    except Exception as e:
        logger.error(f"Think Mode optimization error: {e}", exc_info=True)
        await processing_msg.edit_text(f"❌ Optimization failed: {str(e)}")

    return ConversationHandler.END


async def send_optimized_prompt(update: Update, result: dict):
    """Send the optimized prompt to the user."""
    # Create clean prompt file
    file_content = result['optimized']
    file_buffer = BytesIO(file_content.encode('utf-8'))
    file_buffer.name = f"optimized_prompt_{result['vendor']}.txt"

    # Send info message
    info_message = f"""✅ <b>Optimization Complete!</b>

<b>Vendor:</b> {result['vendor'].upper()}
<b>Format:</b> {result['metadata'].get('format', 'N/A')}
<b>Recommended Model:</b> {result['metadata'].get('model_recommendation', 'N/A')}
<b>Temperature:</b> {result['metadata'].get('temperature_recommendation', 'N/A')}

<b>Enhancement Notes:</b>
{result['enhancement_notes']}

📎 Clean prompt attached - ready to copy & paste!"""

    await update.effective_message.reply_text(info_message, parse_mode='HTML')
    await update.effective_message.reply_document(
        document=file_buffer,
        filename=f"optimized_prompt_{result['vendor']}.txt"
    )

    # Send credits
    credits = """🤖 Prompt optimized by <b>Local LLM Prompt Optimizer</b>

👨‍💻 Created by <a href="https://t.me/Danil_Silantyev">Danil Silantyev</a>
🌐 <a href="https://t.me/DevsOpenNetwork">DevsOpenNetwork</a>"""

    await update.effective_message.reply_text(credits, parse_mode='HTML', disable_web_page_preview=True)


async def cancel_think_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel Think Mode conversation."""
    await update.message.reply_text("Think Mode cancelled. Send a new prompt to start over.")
    return ConversationHandler.END


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment")
        return

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Think Mode conversation handler
    think_mode_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(think_num_questions, pattern="^think:\\d+$")],
        states={
            ANSWERING_QUESTIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_think_mode)],
        per_chat=True,
        per_user=True,
        per_message=False,
        allow_reentry=True
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("optimize", start))

    # Think Mode handlers - MUST be before general text handler
    application.add_handler(CallbackQueryHandler(think_mode_start, pattern="^think_mode$"))
    application.add_handler(CallbackQueryHandler(think_vendor_callback, pattern="^think_vendor:"))
    application.add_handler(think_mode_conversation)

    # General handlers - AFTER conversation handlers
    application.add_handler(CallbackQueryHandler(vendor_callback, pattern="^vendor:"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.add_error_handler(error_handler)

    # Start bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
