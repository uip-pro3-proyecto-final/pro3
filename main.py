#Arquimedes Escart�n
#8-863-235
#Software de restaurante en el que por cierta calificacion de servicio se introduce una cifra de donacion/propina
#y se le hace beneficio a una ONG
import kivy
kivy.require('1.9.0')
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window


# Filtros donde se ingresa valor de entrada de 1-5.
class OneToFiveInput(TextInput):
    pat = re.compile('[^1-5]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        s = s[:1 - len(self.text)]
        return super(OneToFiveInput, self).insert_text(s, from_undo=from_undo)


# Filtros ingresan valor de entrada para un flotante.
class FloatInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class RestaurantFinoFino(App):
    def build(self):
        global starting_tip
        starting_tip = 10

        # Dise�o/Layout.
        Window.clearcolor = (1, 1, 1, 1)
        controls = AnchorLayout(
            anchor_x='right',
            anchor_y='top',
        )
        box = BoxLayout(
            orientation='vertical',
            padding=10,
        )

        # T�tulo.
        apptitle = Label(
            text='Restaurante FinoFino',
            font_size=20,
            shorten=True,
            halign='left',
            strip=True,
            color=[0, 0, 0, 1],
        )

        service_rating_label = Label(
            text='De la escala del 1 al 5 c�mo usted calificaria el servicio?',
            font_size=18,
            color=[0, 0, 0, 1],
        )
        service_rating = OneToFiveInput(
            font_size=18,
            multiline=False,
            input_type='number',
            hint_text='Introduce un numero del 1 al 5',
        )

        food_rating_label = Label(
            text='De la escala del 1 al 5 c�mo usted calificaria la comida?',
            font_size=18,
            color=[0, 0, 0, 1],
        )
        food_rating = OneToFiveInput(
            font_size=18,
            multiline=False,
            input_type='number',
            hint_text='Introduce un numero del 1 al 5',
        )

        # Costo de la comida.
        food_cost_label = Label(
            text='Cuanto costo la comida?',
            font_size=18,
            color=[0, 0, 0, 1],
        )
        food_cost = FloatInput(
            font_size=18,
            hint_text='Introduce el precio sin "$"',
        )

        # Boton de calculo.
        input_btn = Button(
            text='Calculando Donacion',
            font_size=20,
            size_hint_x=None,
            width=200,
            background_color=[0, 1.7, 0, 1]
        )

        # Ajustando la cifra a donar.
        def adjust_tip(rating):
            global starting_tip
            if rating == 1:
                starting_tip = starting_tip - 5
            elif rating == 2:
                starting_tip = starting_tip - 2.5
            elif rating == 3:
                starting_tip = starting_tip + 2.5
            elif rating == 4:
                starting_tip = starting_tip + 3.5
            else:
                starting_tip = starting_tip + 5
            return starting_tip

        # Calculate la donacion y porcentaje de la donacion.
        def calculate_tip(instance):
            service_rating_value = float(service_rating.text)
            food_rating_value = float(food_rating.text)
            adjust_tip(service_rating_value)
            adjust_tip(food_rating_value)

            meal_cost = float(food_cost.text)
            tip = meal_cost * (starting_tip/100)
            format_tip = "${:.2f}".format(tip)
            popup = Popup(
                title='Donacion sugerida',
                content=Label(
                    text='Su donacion sugerida es\n ' + str(starting_tip) + '%\n' + 'Que es ' + str(format_tip),
                    multiline=True,
                ),
                size_hint=(None, None),
                size=(300, 200),
                font_size=18,
            )
            popup.open()

        input_btn.bind(on_press=calculate_tip)

        # Diseno
        controls.add_widget(box)
        box.add_widget(apptitle)
        box.add_widget(service_rating_label)
        box.add_widget(service_rating)
        box.add_widget(food_rating_label)
        box.add_widget(food_rating)
        box.add_widget(food_cost_label)
        box.add_widget(food_cost)
        box.add_widget(input_btn)

        return controls

if __name__ == '__main__':
    RestaurantFinoFino().run()
__version__ = "0.0.1"
