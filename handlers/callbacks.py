from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.product_utils import get_product_by_name
from utils.order_utils import save_order

def register_callbacks(bot):
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
            bot.send_message(call.message.chat.id, "El producto no está disponible.")

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
                f"✅ Has seleccionado {product_name}.\n"
                f"💰 Precio: {product['price']}€\n\n"
                "Ahora, usa /pago para ver los métodos de pago."
            )
        else:
            bot.send_message(call.message.chat.id, "Lo siento, este producto no está disponible o está agotado.")
