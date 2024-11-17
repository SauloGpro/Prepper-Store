from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from utils.product_utils import load_products, get_product_by_name
from utils.order_utils import save_order, get_pending_order_by_user

def register_commands(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(
            message,
            "¡Bienvenido a nuestra tienda en Telegram! 🎉\n"
            "Usa los siguientes comandos para interactuar:\n"
            "👉 /productos - Ver lista de productos\n"
            "👉 /pedido - Realizar una compra\n"
            "👉 /pago - Métodos de pago\n"
        )
    
    @bot.message_handler(commands=['productos'])
    def send_products(message):
        products = load_products()
        if not products:
            bot.reply_to(message, "⚠️ No hay productos disponibles en este momento.")
            return

        for product in products:
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton("Detalles", callback_data=f"detalle_{product['name']}")
            markup.add(button)
            bot.send_message(
                message.chat.id,
                f"🔹 {product['name']}\n💰 Precio: {product['price']}€\n📦 Stock: {product['stock']}",
                reply_markup=markup
            )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("detalle_"))
    def show_product_details(call):
        product_name = call.data.split("_")[1]
        product = get_product_by_name(product_name)

        if product:
            markup = InlineKeyboardMarkup()
            select_button = InlineKeyboardButton("Seleccionar", callback_data=f"seleccionar_{product['name']}")
            markup.add(select_button)
            bot.send_message(
                call.message.chat.id,
                f"📜 Detalles de {product['name']}:\n"
                f"{product['description']}\n\n"
                f"💰 Precio: {product['price']}€\n"
                f"📦 Stock disponible: {product['stock']}\n\n"
                "Haz clic en 'Seleccionar' para proceder con la compra.",
                reply_markup=markup
            )
        else:
            bot.send_message(call.message.chat.id, "⚠️ El producto no está disponible.")
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith("seleccionar_"))
    def confirm_selection(call):
        product_name = call.data.split("_")[1]
        product = get_product_by_name(product_name)

        if product and product["stock"] > 0:
            save_order({
                "user_id": call.from_user.id,
                "username": call.from_user.username,
                "product": product_name,
                "price": product["price"],
                "status": "pendiente"
            })
            bot.send_message(
                call.message.chat.id,
                f"✅ Has seleccionado *{product_name}*.\n"
                f"💰 Total: {product['price']}€\n\n"
                "Por favor, usa /pago para completar el proceso de compra.",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(call.message.chat.id, "⚠️ Lo siento, este producto no está disponible o está agotado.")
    
    @bot.message_handler(commands=['pedido'])
    def realizar_pedido(message):
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        products = load_products()
        for product in products:
            markup.add(KeyboardButton(product["name"]))
        
        bot.reply_to(
            message, 
            "Selecciona un producto para realizar tu pedido:", 
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: is_product_name(message.text))
    def confirmar_pedido(message):
        product_name = message.text
        product = get_product_by_name(product_name)

        if not product or product["stock"] <= 0:
            bot.reply_to(message, "⚠️ Lo siento, este producto no está disponible.")
            return
        
        # Guardar pedido en orders.json
        order = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "product": product_name,
            "price": product["price"],
            "status": "pendiente"
        }
        save_order(order)

        # Mensaje de confirmación
        bot.reply_to(
            message,
            f"Tu pedido de {product_name} ha sido registrado. ✅\n"
            f"💰 Total: {product['price']}€\n"
            "Por favor, realiza el pago usando los métodos que te indicaré con /pago."
        )
    
    @bot.message_handler(commands=['pago'])
    def mostrar_pago(message):
        order = get_pending_order_by_user(message.from_user.id)
        if not order:
            bot.reply_to(message, "⚠️ No tienes ningún pedido pendiente. Selecciona un producto primero con /productos.")
            return

        bot.reply_to(
            message,
            f"💳 Métodos de Pago para tu pedido de *{order['product']}*:\n\n"
            "1. Wise: Enviar a la cuenta XXXX-XXXX\n"
            "2. Criptomonedas: Dirección de wallet ABCD1234\n\n"
            f"💰 Total: {order['price']}€\n\n"
            "Por favor, envía la confirmación de tu pago escribiendo:\n"
            f"👉 *Pago realizado para el pedido de {order['product']}.*",
            parse_mode="Markdown"
        )
    
# Funciones auxiliares
def is_product_name(product_name):
    products = load_products()
    return any(product["name"] == product_name for product in products)


