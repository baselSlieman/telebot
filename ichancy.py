import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update,error
from telegram.ext import ApplicationBuilder,ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext,CallbackQueryHandler
from telegram.error import TimedOut
# from rembg import remove
import requests

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOKEN = "7654562303:AAF5LToQwvIpC08kC167GN3BNoFAXgZS8qw"
base_url = "https://demo92.visual-host.com/api/"
# FIRST_QUESTION, SECOND_QUESTION = range(2)
FIRST_QUESTION, SECOND_QUESTION, THIRD_QUESTION, FOURTH_QUESTION, FIFTH_QUESTION, SIXTH_QUESTION,SEVENTH_QUESTION,EIGHTH_QUESTION  = range(8)
CHAT_TIMEOUT=300

headers = {
    'Content-Type': 'application/json', 
    'Accept': 'application/json',  # نوع المحتوى
    'Authorization': 'Bearer 2|ASAuZhU3p1PHeLOfteuXWR6KTuPuaqsDk4h9hfEb01914cf0'  # معلومات المصادقة مع access token
}
# 1|JrqSlcvhpxY6Gdv2Wiggyrg7n3Fd8Q16mza8AeArc249fbcf
main_keyboard = [
                    [KeyboardButton('🌳 Ichancy | ايشانسي 🌳')], [KeyboardButton('شحن في البوت 🔽'),KeyboardButton('سحب من البوت 🔼')],
                    [KeyboardButton('💵 الرصيد'),KeyboardButton('📋 الشروط والأحكام')],
                    [KeyboardButton('📨 تواصل مع الدعم')]
            ]
def create_keyboard(keyboard):
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
def create_inline_keyboard(keyboard):
        return InlineKeyboardMarkup(keyboard)

## commends functions for inlinKeyboardButons
async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split(':')
    if data[0] == "undoWithdraw":
        response = requests.post(base_url+"undo_withdraw",json={"withdrawId":data[1]},headers=headers)
        if response.status_code == 200 and (response.json())['status']=="success":
            await query.edit_message_text(text=f"🔅 تم التراجع عن الطلب ذو المعرف: {data[1]} بنجاح")
        elif response.status_code == 200 and (response.json())['status']=="failed":
            await query.edit_message_text(text=f"⛔️ {(response.json())['message']}")
        else:
            await query.edit_message_text(text=f"⛔️ حدث خطأ أثناء عملية التراجع")
    await query.answer()
    

# context: bot info # update: update indo
async def start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="⏳ يتم بدء البوت، الرجاء الانتظار...")
    data = {
        'id': update.effective_chat.id,
        'username': update.effective_chat.username,
        'first_name': update.effective_chat.first_name,
        'last_name': update.effective_chat.last_name
    }
    try:
        response = requests.post(base_url+"start",json=data,headers=headers)
        response.raise_for_status()
        if response.status_code==200:
            response_json = response.json()
            if response_json['status']=="success":
                await context.bot.send_message(chat_id=update.effective_chat.id,text="مرحبا بك في بوت You Chance",reply_markup=create_keyboard(main_keyboard))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,text="خطأ أثناء بدء البوت، الرجاء البدء من جديد")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    except requests.exceptions.RequestException as e:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="⚠️ البوت يخضع للصيانة حالياً، الرجاء المحاولة في وقتٍ لاحق")

# handle_message بشكل عام
# async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id,text=update)



async def syriatel(update: Update, context: CallbackContext):
    return FIRST_QUESTION

async def keyboard_button_click(update: Update, context: CallbackContext):
    user_choice = update.message.text
    if user_choice == '🌳 Ichancy | ايشانسي 🌳':
        response = requests.post(base_url+"ichancy",json={"chat_id":update.effective_chat.id},headers=headers)
        if response.status_code==200 :
            response_msg = response.json()
            if response_msg['message'] == "notexist":
                keyboard = [
                    [KeyboardButton('إنشاء حساب')], [KeyboardButton('الرئيسية')],
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text="ليس لديك حساب",reply_markup=create_keyboard(keyboard))
            elif response_msg['message'] == "requested":
                keyboard = [
                    [KeyboardButton('الرئيسية')]
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text="لقد طلبت للتو إنشاء حساب، وسيتم إرساله لك في أقرب وقت",reply_markup=create_keyboard(keyboard))
            elif response_msg['message'] == "exist":
                keyboard = [
                    [KeyboardButton('السحب من الحساب'),KeyboardButton('شحن الحساب')],[KeyboardButton('رصيد أيشانسي'),KeyboardButton('الرئيسية')]
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text=f"الحساب: {response_msg["username"]}",reply_markup=create_keyboard(keyboard))
            elif response_msg['message'] == "error_playerId":
                keyboard = [
                    [KeyboardButton('الرئيسية')]
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text="فشل الحصول على معرف الحساب، الرجاء إعادة المحاولة",reply_markup=create_keyboard(keyboard))
            else:
                keyboard = [
                    [KeyboardButton('الرئيسية')]
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text=f"حدث الخطأ التالي: {response_msg['message']}",reply_markup=create_keyboard(keyboard))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    elif user_choice == 'شحن في البوت 🔽':
        keyboard = [
            [KeyboardButton('سيريتل كاش'),KeyboardButton('MTN كاش')], [KeyboardButton('بنك بيمو'),KeyboardButton('الرئيسية')],
        ]
        await context.bot.send_message(chat_id=update.effective_chat.id,text="🔻 أقل قيمة للشحن هي 5,000 🔻\nوأي قيمة أقل من 5,000 لا يمكن شحنها أو استرجاعها\n\nاختر طريقة الدفع:",reply_markup=create_keyboard(keyboard))
    elif user_choice == 'سيريتل كاش':
         await context.bot.send_message(chat_id=update.effective_chat.id,text="كود التحويل: <b><code>28274537</code></b>", parse_mode='HTML')
         await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل المبلغ")
         context.user_data['current_state'] = FIRST_QUESTION
         return FIRST_QUESTION
    elif user_choice in ("MTN كاش","بنك بيمو"):
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f"⛔️ <b>طريقة الدفع: {user_choice}، غير متاحة حالياً</b>", parse_mode='HTML')
    elif user_choice == 'الرئيسية':
         await context.bot.send_message(chat_id=update.effective_chat.id,text="اختر إجراء:", reply_markup=create_keyboard(main_keyboard))
         return ConversationHandler.END
    elif user_choice == 'رصيد أيشانسي':
         response = requests.post(base_url+"getIchancyBalance",json={"chat_id":update.effective_chat.id},headers=headers)
         if response.status_code == 200:
            response_msg = response.json()
            await context.bot.send_message(chat_id=update.effective_chat.id,text=response_msg["message"])
         else:
            await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")    
    elif user_choice == '💵 الرصيد':
         response = requests.post(base_url+"getMyBalance",json={"chat_id":update.effective_chat.id},headers=headers)
         if response.status_code == 200:
            response_msg = response.json()
            await context.bot.send_message(chat_id=update.effective_chat.id,text=f"💵 رصيدك الحالي في البوت: {response_msg["balance"]} NSP")
         else:
            await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    elif user_choice == 'شحن الحساب':
         response = requests.post(base_url+"getMyBalance",json={"chat_id":update.effective_chat.id},headers=headers)
         if response.status_code == 200:
            response_msg = response.json()
            keyboard = [
                    [KeyboardButton('الرئيسية')],
                ]
            await context.bot.send_message(chat_id=update.effective_chat.id,text=f"رصيدك الحالي في البوت: {response_msg["balance"]} NSP \n أدخل مبلغ الحشن:",reply_markup=create_keyboard(keyboard))
            context.user_data['current_state'] = FIFTH_QUESTION
            return FIFTH_QUESTION
    elif user_choice == 'السحب من الحساب':
            keyboard = [
                    [KeyboardButton('الرئيسية')],
            ]
            await context.bot.send_message(chat_id=update.effective_chat.id,text=f"أدخل مبلغ السحب:",reply_markup=create_keyboard(keyboard))
            context.user_data['current_state'] = SIXTH_QUESTION
            return SIXTH_QUESTION
    elif user_choice == '📨 تواصل مع الدعم':
        await context.bot.send_message(chat_id=update.effective_chat.id,text="@Bass889h",reply_markup=create_keyboard(main_keyboard))
    elif user_choice == 'سحب من البوت 🔼':
            keyboard = [
                    [KeyboardButton('الرئيسية')],
            ]
            await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل كود التحويل الخاص بك:",reply_markup=create_keyboard(keyboard))
            context.user_data['current_state'] = SEVENTH_QUESTION
            return SEVENTH_QUESTION
    elif user_choice == '📋 الشروط والأحكام':
            keyboard = [
                    [KeyboardButton('الرئيسية')],
            ]
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="""شروط وأحكام يجب عليك معرفتها قبل استخدام youChanc Bot. 
1_البوت مخصّص لإنشاء الحسابات والسّحب والتعبئة الفورية لموقع Ichancy .
2_انشاء أكثر من حساب يعرّض جميع الحسابات للحظر وتجميد الرصيد الموجود في الحسابات بحسب شروط واحكام الموقع للحد من الانشطة الاحتيالية بناءاً على سياسة اللعب النظيف . 
3_لايحق للاعب شحن وسحب رصيد بقصد التبديل بين طرق الدفع ويحق لإدارة البوت سحب أي رصيد والتحفّظ عليه عند وجود عمليّة تبديل أو أي مخالفة لقوانين البوت . 
4- يتم حساب ارباح الاحالات عند وجود 3 إحالات نشطة او أكثر""",
                reply_markup=create_keyboard(keyboard))
    elif user_choice == 'إنشاء حساب':
        response = requests.post(base_url+"checkbalance",json={"chat_id":update.effective_chat.id},headers=headers)
        if response.status_code == 200:
            response_msg = response.json()
            if response_msg['status']=="success":
                keyboard = [
                    [KeyboardButton('الرئيسية')],
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text="أخل اسم المستخدم",reply_markup=create_keyboard(keyboard))
                context.user_data['current_state'] = THIRD_QUESTION
                return THIRD_QUESTION
            else:
                keyboard = [
                    [KeyboardButton('الرئيسية')],
                ]
                await context.bot.send_message(chat_id=update.effective_chat.id,text="يجب أن يتوفر في رصيد 10,000 NSP على الأقل لإنشاء حساب",reply_markup=create_keyboard(keyboard))
        

async def third_question(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text
    context.user_data['response_to_question3'] = user_response
    context.user_data['current_state'] = FOURTH_QUESTION
    await update.message.reply_text("أدخل كلمة المرور: (8 محارف على الأقل)")
    return FOURTH_QUESTION

async def fourth_question(update: Update, context: CallbackContext) -> int:
    keyboard = [
            [KeyboardButton('الرئيسية')],
    ]
    
    user_response = update.message.text
    context.user_data['response_to_question4'] = user_response
    await context.bot.send_message(chat_id=update.effective_chat.id,text="⏳ جاري معالجة...")
    response_to_question3 = context.user_data['response_to_question3']
    response_to_question4 = context.user_data['response_to_question4']
    try:
        response = requests.post(base_url+"newichaccount_v2",json={"chat_id":update.effective_chat.id,"e_username":response_to_question3,"e_password":response_to_question4},headers=headers)
        if response.status_code== 200:
            response_json = response.json()
            await context.bot.send_message(chat_id=update.effective_chat.id,text=response_json["message"],reply_markup=create_keyboard(keyboard), parse_mode='HTML')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
        return ConversationHandler.END  
    except TimedOut:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="لقد تجاوز طلبك الزمن المحدد له ، الرجاء المحاولة مرة أخرى.")
        return ConversationHandler.END
    except Exception as e:
        print(f"حدث خطأ: {e}")

async def first_question(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text
    context.user_data['response_to_question1'] = user_response
    context.user_data['current_state'] = SECOND_QUESTION
    await update.message.reply_text("أدخل رقم عملية الدفع")
    return SECOND_QUESTION

async def second_question(update: Update, context: CallbackContext) -> int:
    keyboard = [
            [KeyboardButton('الرئيسية')],
    ]
    
    user_response = update.message.text
    context.user_data['response_to_question2'] = user_response
    await context.bot.send_message(chat_id=update.effective_chat.id,text="⏳ جاري معالجة الطلب...")
    response_to_question1 = context.user_data['response_to_question1']
    response_to_question2 = context.user_data['response_to_question2']
    response = requests.post(base_url+"charge",json={"chat_id":update.effective_chat.id,"amount":response_to_question1,"processid":response_to_question2},headers=headers)
    if response.status_code== 200:
        response_json = response.json()
        await context.bot.send_message(chat_id=update.effective_chat.id,text=response_json["message"],reply_markup=create_keyboard(keyboard))
        if response_json["status"]== "failed":
            await context.bot.send_message(chat_id=update.effective_chat.id,text="إعادة المحاولة \n إدخال مبلغ الدفع:")
            return FIRST_QUESTION
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    return ConversationHandler.END

async def fifth_question(update: Update, context: CallbackContext) -> int:
    keyboard = [
            [KeyboardButton('الرئيسية')],
    ]
    user_response = update.message.text
    context.user_data['response_to_question5'] = user_response
    context.user_data['current_state'] = FIFTH_QUESTION
    await context.bot.send_message(chat_id=update.effective_chat.id,text="⏳ جاري معالجة الطلب...")
    response_to_question5 = context.user_data['response_to_question5']
    response = requests.post(base_url+"charge_ichancy",json={"chat_id":update.effective_chat.id,"amount":response_to_question5,"type":"charge"},headers=headers)
    if response.status_code== 200:
        response_json = response.json()
        await context.bot.send_message(chat_id=update.effective_chat.id,text=response_json["message"],reply_markup=create_keyboard(keyboard))
        if response_json["status"]== "balance":
            return FIFTH_QUESTION
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    return ConversationHandler.END

async def sixth_question(update: Update, context: CallbackContext) -> int:
    keyboard = [
            [KeyboardButton('الرئيسية')],
    ]
    user_response = update.message.text
    context.user_data['response_to_question6'] = user_response
    context.user_data['current_state'] = SIXTH_QUESTION
    await context.bot.send_message(chat_id=update.effective_chat.id,text="⏳ جاري معالجة الطلب...")
    response_to_question6 = context.user_data['response_to_question6']
    response = requests.post(base_url+"withdraw_ichancy",json={"chat_id":update.effective_chat.id,"amount":response_to_question6,"type":"withdraw"},headers=headers)
    if response.status_code== 200:
        response_json = response.json()
        await context.bot.send_message(chat_id=update.effective_chat.id,text=response_json["message"],reply_markup=create_keyboard(keyboard))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    return ConversationHandler.END

async def seventh_question(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text
    context.user_data['response_to_question7'] = user_response
    context.user_data['current_state'] = EIGHTH_QUESTION
    await update.message.reply_text("أدخل مبلغ السحب:")
    return  EIGHTH_QUESTION

async def eighth_question(update: Update, context: CallbackContext) -> int:
    keyboard = [
            [KeyboardButton('الرئيسية')],
    ]
    user_response = update.message.text
    context.user_data['response_to_question8'] = user_response
    await context.bot.send_message(chat_id=update.effective_chat.id,text="⏳ جاري معالجة الطلب...")
    response_to_question7 = context.user_data['response_to_question7']
    response_to_question8 = context.user_data['response_to_question8']
    response = requests.post(base_url+"withdraw",json={"chat_id":update.effective_chat.id,"amount":response_to_question8,"code":response_to_question7},headers=headers)
    if response.status_code== 200:
        response_json = response.json()
        await context.bot.send_message(chat_id=update.effective_chat.id,text=response_json["message"],reply_markup=create_keyboard(keyboard))
        if response_json["status"]== "success":
            await context.bot.send_message(chat_id=update.effective_chat.id,text="❗️ يمكنك التراجع عن طلب السحب",reply_markup=create_inline_keyboard([[InlineKeyboardButton('↩️ تراجع',callback_data=f'undoWithdraw:{response_json['withdrawId']}')]]))
        if response_json["status"]== "balance":
            await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل مبلغ سحب بكافئ رصيدك الحالي في البوت أو دون:")
            return EIGHTH_QUESTION
        if response_json["status"]== "minvalue":
            await context.bot.send_message(chat_id=update.effective_chat.id,text="أعد إدخال المبلغ:")
            return EIGHTH_QUESTION
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="البوت يواجه مشكلة بالاتصال بالسيرفر، الرجاء المحاولة في وقتٍ لاحق")
    return ConversationHandler.END 

      
# async def first_question(update: Update, context: CallbackContext) -> int:
#     user_response = update.message.text
#     context.user_data['response_to_question1'] = user_response
#     await update.message.reply_text("سؤال آخر؟")
#     return SECOND_QUESTION

# async def second_question(update: Update, context: CallbackContext) -> int:
#     user_response = update.message.text
#     context.user_data['response_to_question2'] = user_response
#     await update.message.reply_text("شكرًا لك. تم استلام الإجابات.")

    # يمكنك هنا استخدام الإجابات بالطريقة التي ترغب فيها
    
async def fallback(update: Update, context: CallbackContext) -> int:
    # if context.error.message == 'Timed out':
    #    update.message.reply_text("تجاوز الوقت المسموح للحفظ، الرجاء البدء من جديد.")
    user_response = update.message.text
    if user_response=="إنهاء":
        # keyboard = [
        #     [KeyboardButton('سيريتل كاش'),KeyboardButton('MTN كاش')], [KeyboardButton('بنك بيمو'),KeyboardButton('الرئيسية')],
        # ]
        await context.bot.send_message(chat_id=update.effective_chat.id,text="اختر إجراء:",reply_markup=create_keyboard(main_keyboard))
        
        return ConversationHandler.END
    if user_response== "الرئيسية":
        await context.bot.send_message(chat_id=update.effective_chat.id,text="اختر إجراء:", reply_markup=create_keyboard(main_keyboard))
        return ConversationHandler.END
    
   

    keyboard = [
            [KeyboardButton('إنهاء')],
        ]
    
    # Get the current state of the conversation
    current_state = context.user_data.get('current_state', FIRST_QUESTION)

    # Redirect the user to the last question asked
    if current_state == FIRST_QUESTION:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل مبلغ صحيح:",reply_markup=create_keyboard(keyboard))
        return FIRST_QUESTION
    elif current_state == SECOND_QUESTION:
        await update.message.reply_text("أدخل رقم عملية الدفع",reply_markup=create_keyboard(keyboard))
        return SECOND_QUESTION
    elif current_state == THIRD_QUESTION:
        await update.message.reply_text("أدخل اسم المستخدم",reply_markup=create_keyboard(keyboard))
        return THIRD_QUESTION
    elif current_state == FOURTH_QUESTION:
        await update.message.reply_text("طول كلمة المرور 8 على الأقل\n أعد إدخال كلمة مرور صحيحة:",reply_markup=create_keyboard(keyboard))
        return FOURTH_QUESTION
    if current_state == FIFTH_QUESTION:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل مبلغ صحيح:",reply_markup=create_keyboard(keyboard))
        return FIFTH_QUESTION
    if current_state == SIXTH_QUESTION:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل مبلغ صحيح:",reply_markup=create_keyboard(keyboard))
        return SIXTH_QUESTION
    if current_state == SEVENTH_QUESTION:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل كود التحويل الخاص بك",reply_markup=create_keyboard(keyboard))
        return SEVENTH_QUESTION
    if current_state == EIGHTH_QUESTION:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="أدخل مبلغ صحيح",reply_markup=create_keyboard(keyboard))
        return EIGHTH_QUESTION
        
    else:
        await update.message.reply_text("⛔️ عذرًا، لم أتمكن من فهم طلبك. يرجى استخدام الأوامر المتاحة والإجابة بشكل صحيح .")
        return ConversationHandler.END
    
    
async def timeout(update:Update, context:CallbackContext):
   await update.message.reply_text('انتهى الوقت المخصص لإجابتك , الرجاء البدء من جديد')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    # application.updater.bot.get_updates(timeout=2)
    # commend handlers
    start_handler = CommandHandler('start',start)
    # message_handler = MessageHandler(filters.ALL,keyboard_button_click)

    # message handler
    # message_handler = MessageHandler(filters.ALL,handle_message)  # بشكل عام
    # message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE,handle_message)
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.ALL,keyboard_button_click)],
        states={
            FIRST_QUESTION: [MessageHandler(filters.TEXT & filters.Regex(r'^([\s\d]+)$'), first_question)],
            SECOND_QUESTION: [MessageHandler(filters.TEXT & filters.Regex(r'^([\s\d]+)$'), second_question)],
            THIRD_QUESTION: [MessageHandler(filters.TEXT & ~filters.Text(["الرئيسية", "إنهاء"]), third_question)],
            FOURTH_QUESTION: [MessageHandler(filters.TEXT & filters.Regex(r".{8,}"), fourth_question)],
            FIFTH_QUESTION: [MessageHandler(filters.TEXT & filters.Regex(r'^([\s\d]+)$'), fifth_question)],
            SIXTH_QUESTION: [MessageHandler(filters.TEXT & filters.Regex(r'^([\s\d]+)$'), sixth_question)],
            SEVENTH_QUESTION: [MessageHandler(filters.TEXT & ~filters.Text(["الرئيسية", "إنهاء"]), seventh_question)],
            EIGHTH_QUESTION: [MessageHandler(filters.TEXT & filters.Regex(r'^([\s\d]+)$'),eighth_question)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.TEXT | filters.COMMAND, timeout)],
        },
        fallbacks=[MessageHandler(filters.ALL, fallback)],
        conversation_timeout=CHAT_TIMEOUT
    )
    application.add_handler(CallbackQueryHandler(button_click))
    
    # register commend
    application.add_handler(start_handler)
    # application.add_handler(message_handler)
    application.add_handler(conv_handler)
    # application.add_handler(message_handler)
    # يبقي على البوت شغال
    try:
        
        application.run_polling(close_loop=False)
    except error.TimedOut:
        print('TimedOut trying again')
























# notes:
# pip install rembg
# pip install python-telegram-bot
