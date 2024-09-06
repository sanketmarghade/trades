<<<<<<< HEAD
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from tradingview_ta import TA_Handler, Interval
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import yfinance as yf
from io import BytesIO
from kivy.core.image import Image as CoreImage

# Define interval options
INTERVAL_OPTIONS = {
    "1 Minute": Interval.INTERVAL_1_MINUTE,
    "5 Minutes": Interval.INTERVAL_5_MINUTES,
    "15 Minutes": Interval.INTERVAL_15_MINUTES,
    "30 Minutes": Interval.INTERVAL_30_MINUTES,
    "1 Hour": Interval.INTERVAL_1_HOUR,
    "2 Hours": Interval.INTERVAL_2_HOURS,
    "4 Hours": Interval.INTERVAL_4_HOURS,
    "1 Day": Interval.INTERVAL_1_DAY,
    "1 Week": Interval.INTERVAL_1_WEEK,
    "1 Month": Interval.INTERVAL_1_MONTH
}

KV = '''
ScreenManager:
    InputScreen:
    ResultScreen:
    ChartScreen:
    ConnectionErrorScreen:

<InputScreen>:
    name: 'input_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.2, 0.3, 0.4, 1

        MDLabel:
            text: "Trading Analysis"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDCard:
            orientation: 'vertical'
            size_hint: (1, None)
            height: 250
            padding: 20
            spacing: 20
            pos_hint: {"center_x": .5}
            md_bg_color: 0.9, 0.9, 0.9, 1

            MDTextField:
                id: symbol_input
                hint_text: "Enter the trading symbol (e.g., 'AAPL')"
                helper_text: "Trading Symbol"
                helper_text_mode: "on_focus"
                size_hint_y: None
                height: 40

            MDLabel:
                text: "Select Interval"
                halign: "left"
                size_hint_y: None
                height: 30
                theme_text_color: "Custom"
                text_color: 0.3, 0.3, 0.3, 1

            Spinner:
                id: interval_spinner
                text: "Select Interval"
                values: ["1 Minute", "5 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "1 Day", "1 Week", "1 Month"]
                size_hint_y: None
                height: 44
                on_text: root.set_interval(self.text)

            MDRaisedButton:
                text: "Get Analysis"
                pos_hint: {"center_x": .5}
                on_release: app.get_analysis()
                size_hint_y: None
                height: 50
                md_bg_color: 0.1, 0.6, 0.4, 1
                text_color: 1, 1, 1, 1

<ResultScreen>:
    name: 'result_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDLabel:
            text: "Analysis Results"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1

        ScrollView:
            size_hint: (1, 0.9)
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 10

                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 20
                    spacing: 10
                    md_bg_color: 1, 1, 1, 1
                    
                    MDLabel:
                        id: summary_label
                        text: "Summary will be shown here"
                        theme_text_color: "Custom"
                        text_color: 0.1, 0.1, 0.1, 1
                        halign: "left"
                        size_hint_y: None
                        height: self.texture_size[1] + 10

                    MDLabel:
                        id: indicators_label
                        text: "Indicators will be shown here"
                        theme_text_color: "Custom"
                        text_color: 0.1, 0.1, 0.1, 1
                        halign: "left"
                        size_hint_y: None
                        height: self.texture_size[1] + 10

        MDRaisedButton:
            text: "Show Chart"
            pos_hint: {"center_x": .5}
            on_release: app.show_chart()
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: "Back to Input"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'input_screen'
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1

<ChartScreen>:
    name: 'chart_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDLabel:
            text: "Line Chart"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1

        Image:
            id: chart_image
            source: ""
            allow_stretch: True
            keep_ratio: False

        MDRaisedButton:
            text: "Back to Result"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'result_screen'
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1

<ConnectionErrorScreen>:
    name: 'connection_error_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 1, 0.2, 0.2, 1

        MDLabel:
            text: "Connection Error"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDLabel:
            id: error_message_label
            text: "Unable to connect to the server. Please check your internet connection."
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: "Back to Input"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'input_screen'
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1
'''

class InputScreen(Screen):
    selected_interval = Interval.INTERVAL_1_DAY  # Default interval

    def set_interval(self, interval_text):
        # Map the selected interval text to the corresponding Interval enum value
        self.selected_interval = INTERVAL_OPTIONS.get(interval_text, Interval.INTERVAL_1_DAY)

class ResultScreen(Screen):
    pass

class ChartScreen(Screen):
    pass

class ConnectionErrorScreen(Screen):
    pass

class TradingAnalysisApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input_screen'))
        sm.add_widget(ResultScreen(name='result_screen'))
        sm.add_widget(ChartScreen(name='chart_screen'))
        sm.add_widget(ConnectionErrorScreen(name='connection_error_screen'))
        return Builder.load_string(KV)

    def get_analysis(self):
        input_screen = self.root.get_screen('input_screen')
        symbol_input = input_screen.ids.symbol_input.text.strip().upper()
        selected_interval = input_screen.selected_interval

        if not symbol_input:
            self.root.get_screen('result_screen').ids.summary_label.text = "Error: Trading symbol cannot be empty."
            self.root.get_screen('result_screen').ids.indicators_label.text = ""
            return

        handler = TA_Handler(
            symbol=symbol_input,
            screener="india",
            exchange="NSE",
            interval=selected_interval
        )

        try:
            analysis = handler.get_analysis()
            result_screen = self.root.get_screen('result_screen')
            result_screen.ids.summary_label.text = "Summary:\n" + str(analysis.summary)
            indicators_text = "\n".join([f"{indicator}: {value}" for indicator, value in analysis.indicators.items()])
            result_screen.ids.indicators_label.text = "Indicators:\n" + indicators_text
            self.root.current = 'result_screen'
        except Exception as e:
            print(f"An error occurred: {e}")
            self.root.current = 'connection_error_screen'
            error_screen = self.root.get_screen('connection_error_screen')
            error_screen.ids.error_message_label.text = f"Error: {str(e)}"

    def show_chart(self):
        input_screen = self.root.get_screen('input_screen')
        symbol_input = input_screen.ids.symbol_input.text.strip().upper()
        selected_interval = input_screen.selected_interval

        if not symbol_input:
            return  # Optionally handle this case with an error message

        try:
            # Define period based on interval
            period = {
                Interval.INTERVAL_1_MINUTE: "1d",
                Interval.INTERVAL_5_MINUTES: "5d",
                Interval.INTERVAL_15_MINUTES: "15d",
                Interval.INTERVAL_30_MINUTES: "30d",
                Interval.INTERVAL_1_HOUR: "60d",
                Interval.INTERVAL_2_HOURS: "120d",
                Interval.INTERVAL_4_HOURS: "240d",
                Interval.INTERVAL_1_DAY: "1y",
                Interval.INTERVAL_1_WEEK: "2y",
                Interval.INTERVAL_1_MONTH: "5y"
            }.get(selected_interval, "1y")

            # Fetch historical data from Yahoo Finance
            df = yf.download(symbol_input, period=period, interval=selected_interval.name.lower())

            # Prepare the data for plotting
            fig = go.Figure(data=go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Closing Price'
            ))
            fig.update_layout(
                title=f'Line Chart for {symbol_input}',
                xaxis_title='Date',
                yaxis_title='Price'
            )

            # Convert Plotly figure to PNG image
            img_bytes = BytesIO()
            pio.write_image(fig, img_bytes, format='png')
            img_bytes.seek(0)
            img = CoreImage(img_bytes, ext='png')

            # Display the image in the ChartScreen
            chart_screen = self.root.get_screen('chart_screen')
            chart_screen.ids.chart_image.texture = img.texture

            # Switch to the chart screen
            self.root.current = 'chart_screen'

        except Exception as e:
            print(f"An error occurred while fetching or plotting the chart: {e}")
            self.root.current = 'connection_error_screen'
            error_screen = self.root.get_screen('connection_error_screen')
            error_screen.ids.error_message_label.text = f"Error: {str(e)}"

if __name__ == '__main__':
    TradingAnalysisApp().run()
=======
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from tradingview_ta import TA_Handler, Interval
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import yfinance as yf
from io import BytesIO
from kivy.core.image import Image as CoreImage

# Define interval options
INTERVAL_OPTIONS = {
    "1 Minute": Interval.INTERVAL_1_MINUTE,
    "5 Minutes": Interval.INTERVAL_5_MINUTES,
    "15 Minutes": Interval.INTERVAL_15_MINUTES,
    "30 Minutes": Interval.INTERVAL_30_MINUTES,
    "1 Hour": Interval.INTERVAL_1_HOUR,
    "2 Hours": Interval.INTERVAL_2_HOURS,
    "4 Hours": Interval.INTERVAL_4_HOURS,
    "1 Day": Interval.INTERVAL_1_DAY,
    "1 Week": Interval.INTERVAL_1_WEEK,
    "1 Month": Interval.INTERVAL_1_MONTH
}

KV = '''
ScreenManager:
    InputScreen:
    ResultScreen:
    ChartScreen:
    ConnectionErrorScreen:

<InputScreen>:
    name: 'input_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.2, 0.3, 0.4, 1

        MDLabel:
            text: "Trading Analysis"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDCard:
            orientation: 'vertical'
            size_hint: (1, None)
            height: 250
            padding: 20
            spacing: 20
            pos_hint: {"center_x": .5}
            md_bg_color: 0.9, 0.9, 0.9, 1

            MDTextField:
                id: symbol_input
                hint_text: "Enter the trading symbol (e.g., 'AAPL')"
                helper_text: "Trading Symbol"
                helper_text_mode: "on_focus"
                size_hint_y: None
                height: 40

            MDLabel:
                text: "Select Interval"
                halign: "left"
                size_hint_y: None
                height: 30
                theme_text_color: "Custom"
                text_color: 0.3, 0.3, 0.3, 1

            Spinner:
                id: interval_spinner
                text: "Select Interval"
                values: ["1 Minute", "5 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "4 Hours", "1 Day", "1 Week", "1 Month"]
                size_hint_y: None
                height: 44
                on_text: root.set_interval(self.text)

            MDRaisedButton:
                text: "Get Analysis"
                pos_hint: {"center_x": .5}
                on_release: app.get_analysis()
                size_hint_y: None
                height: 50
                md_bg_color: 0.1, 0.6, 0.4, 1
                text_color: 1, 1, 1, 1

<ResultScreen>:
    name: 'result_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDLabel:
            text: "Analysis Results"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1

        ScrollView:
            size_hint: (1, 0.9)
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 10

                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 20
                    spacing: 10
                    md_bg_color: 1, 1, 1, 1
                    
                    MDLabel:
                        id: summary_label
                        text: "Summary will be shown here"
                        theme_text_color: "Custom"
                        text_color: 0.1, 0.1, 0.1, 1
                        halign: "left"
                        size_hint_y: None
                        height: self.texture_size[1] + 10

                    MDLabel:
                        id: indicators_label
                        text: "Indicators will be shown here"
                        theme_text_color: "Custom"
                        text_color: 0.1, 0.1, 0.1, 1
                        halign: "left"
                        size_hint_y: None
                        height: self.texture_size[1] + 10

        MDRaisedButton:
            text: "Show Chart"
            pos_hint: {"center_x": .5}
            on_release: app.show_chart()
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: "Back to Input"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'input_screen'
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1

<ChartScreen>:
    name: 'chart_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDLabel:
            text: "Line Chart"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1

        Image:
            id: chart_image
            source: ""
            allow_stretch: True
            keep_ratio: False

        MDRaisedButton:
            text: "Back to Result"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'result_screen'
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1

<ConnectionErrorScreen>:
    name: 'connection_error_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 1, 0.2, 0.2, 1

        MDLabel:
            text: "Connection Error"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDLabel:
            id: error_message_label
            text: "Unable to connect to the server. Please check your internet connection."
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1] + 10
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: "Back to Input"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'input_screen'
            size_hint_y: None
            height: 50
            md_bg_color: 0.1, 0.6, 0.4, 1
            text_color: 1, 1, 1, 1
'''

class InputScreen(Screen):
    selected_interval = Interval.INTERVAL_1_DAY  # Default interval

    def set_interval(self, interval_text):
        # Map the selected interval text to the corresponding Interval enum value
        self.selected_interval = INTERVAL_OPTIONS.get(interval_text, Interval.INTERVAL_1_DAY)

class ResultScreen(Screen):
    pass

class ChartScreen(Screen):
    pass

class ConnectionErrorScreen(Screen):
    pass

class TradingAnalysisApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input_screen'))
        sm.add_widget(ResultScreen(name='result_screen'))
        sm.add_widget(ChartScreen(name='chart_screen'))
        sm.add_widget(ConnectionErrorScreen(name='connection_error_screen'))
        return Builder.load_string(KV)

    def get_analysis(self):
        input_screen = self.root.get_screen('input_screen')
        symbol_input = input_screen.ids.symbol_input.text.strip().upper()
        selected_interval = input_screen.selected_interval

        if not symbol_input:
            self.root.get_screen('result_screen').ids.summary_label.text = "Error: Trading symbol cannot be empty."
            self.root.get_screen('result_screen').ids.indicators_label.text = ""
            return

        handler = TA_Handler(
            symbol=symbol_input,
            screener="india",
            exchange="NSE",
            interval=selected_interval
        )

        try:
            analysis = handler.get_analysis()
            result_screen = self.root.get_screen('result_screen')
            result_screen.ids.summary_label.text = "Summary:\n" + str(analysis.summary)
            indicators_text = "\n".join([f"{indicator}: {value}" for indicator, value in analysis.indicators.items()])
            result_screen.ids.indicators_label.text = "Indicators:\n" + indicators_text
            self.root.current = 'result_screen'
        except Exception as e:
            print(f"An error occurred: {e}")
            self.root.current = 'connection_error_screen'
            error_screen = self.root.get_screen('connection_error_screen')
            error_screen.ids.error_message_label.text = f"Error: {str(e)}"

    def show_chart(self):
        input_screen = self.root.get_screen('input_screen')
        symbol_input = input_screen.ids.symbol_input.text.strip().upper()
        selected_interval = input_screen.selected_interval

        if not symbol_input:
            return  # Optionally handle this case with an error message

        try:
            # Define period based on interval
            period = {
                Interval.INTERVAL_1_MINUTE: "1d",
                Interval.INTERVAL_5_MINUTES: "5d",
                Interval.INTERVAL_15_MINUTES: "15d",
                Interval.INTERVAL_30_MINUTES: "30d",
                Interval.INTERVAL_1_HOUR: "60d",
                Interval.INTERVAL_2_HOURS: "120d",
                Interval.INTERVAL_4_HOURS: "240d",
                Interval.INTERVAL_1_DAY: "1y",
                Interval.INTERVAL_1_WEEK: "2y",
                Interval.INTERVAL_1_MONTH: "5y"
            }.get(selected_interval, "1y")

            # Fetch historical data from Yahoo Finance
            df = yf.download(symbol_input, period=period, interval=selected_interval.name.lower())

            # Prepare the data for plotting
            fig = go.Figure(data=go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Closing Price'
            ))
            fig.update_layout(
                title=f'Line Chart for {symbol_input}',
                xaxis_title='Date',
                yaxis_title='Price'
            )

            # Convert Plotly figure to PNG image
            img_bytes = BytesIO()
            pio.write_image(fig, img_bytes, format='png')
            img_bytes.seek(0)
            img = CoreImage(img_bytes, ext='png')

            # Display the image in the ChartScreen
            chart_screen = self.root.get_screen('chart_screen')
            chart_screen.ids.chart_image.texture = img.texture

            # Switch to the chart screen
            self.root.current = 'chart_screen'

        except Exception as e:
            print(f"An error occurred while fetching or plotting the chart: {e}")
            self.root.current = 'connection_error_screen'
            error_screen = self.root.get_screen('connection_error_screen')
            error_screen.ids.error_message_label.text = f"Error: {str(e)}"

if __name__ == '__main__':
    TradingAnalysisApp().run()
>>>>>>> 49c8cb8fb13f7cb91679314ad36eda00f8fbaf68
