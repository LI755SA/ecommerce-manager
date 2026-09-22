from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class Card(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.95, 0.95, 0.97, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class StoreApp(App):

    def build(self):

        main = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        # =========================
        # HEADER
        # =========================

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=85,
            spacing=3
        )

        title = Label(
            text="E-Commerce Manager",
            font_size=27,
            bold=True,
            color=(0.1, 0.1, 0.15, 1)
        )

        subtitle = Label(
            text="Sales & Profit Calculator",
            font_size=14,
            color=(0.4, 0.4, 0.45, 1)
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        main.add_widget(header)

        # =========================
        # INPUT CARD
        # =========================

        input_card = Card(
            orientation="vertical",
            padding=15,
            spacing=10,
            size_hint_y=None,
            height=270
        )

        section_title = Label(
            text="Sale Information",
            font_size=19,
            bold=True,
            color=(0.15, 0.15, 0.2, 1),
            size_hint_y=None,
            height=35
        )

        input_card.add_widget(section_title)

        self.price = TextInput(
            hint_text="Selling price (DA)",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        self.cost = TextInput(
            hint_text="Cost price (DA)",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        self.quantity = TextInput(
            hint_text="Quantity sold",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        self.delivery = TextInput(
            hint_text="Delivery cost (DA) - optional",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        input_card.add_widget(self.price)
        input_card.add_widget(self.cost)
        input_card.add_widget(self.quantity)
        input_card.add_widget(self.delivery)

        main.add_widget(input_card)

        # =========================
        # BUTTONS
        # =========================

        buttons = BoxLayout(
            spacing=10,
            size_hint_y=None,
            height=55
        )

        calculate = Button(
            text="CALCULATE PROFIT",
            font_size=16,
            bold=True
        )

        clear = Button(
            text="CLEAR",
            font_size=15
        )

        calculate.bind(
            on_press=self.calculate_profit
        )

        clear.bind(
            on_press=self.clear_fields
        )

        buttons.add_widget(calculate)
        buttons.add_widget(clear)

        main.add_widget(buttons)

        # =========================
        # RESULT CARD
        # =========================

        result_card = Card(
            orientation="vertical",
            padding=15,
            spacing=5
        )

        result_title = Label(
            text="Results",
            font_size=19,
            bold=True,
            color=(0.15, 0.15, 0.2, 1),
            size_hint_y=None,
            height=35
        )

        self.result = Label(
            text="Enter your data and calculate",
            font_size=16,
            color=(0.25, 0.25, 0.3, 1)
        )

        result_card.add_widget(result_title)
        result_card.add_widget(self.result)

        main.add_widget(result_card)

        return main

    # =========================
    # CALCULATE
    # =========================

    def calculate_profit(self, instance):

        if (
            not self.price.text
            or not self.cost.text
            or not self.quantity.text
        ):
            self.result.text = (
                "Please enter:\n"
                "Selling price, Cost price and Quantity"
            )
            return

        price = int(self.price.text)
        cost = int(self.cost.text)
        quantity = int(self.quantity.text)

        delivery = (
            int(self.delivery.text)
            if self.delivery.text
            else 0
        )

        sales = price * quantity

        product_cost = cost * quantity

        total_expenses = product_cost + delivery

        profit = sales - total_expenses

        if sales > 0:
            profit_margin = (profit / sales) * 100
        else:
            profit_margin = 0

        if profit > 0:
            status = "PROFIT"
        elif profit < 0:
            status = "LOSS"
        else:
            status = "NO PROFIT"

        self.result.text = (
            f"Sales: {sales} DA\n"
            f"Product Cost: {product_cost} DA\n"
            f"Delivery: {delivery} DA\n"
            f"Total Expenses: {total_expenses} DA\n"
            f"Profit: {profit} DA\n"
            f"Profit Margin: {round(profit_margin, 2)}%\n"
            f"Status: {status}"
        )

    # =========================
    # CLEAR
    # =========================

    def clear_fields(self, instance):

        self.price.text = ""
        self.cost.text = ""
        self.quantity.text = ""
        self.delivery.text = ""

        self.result.text = (
            "Enter your data and calculate"
        )


StoreApp().run()