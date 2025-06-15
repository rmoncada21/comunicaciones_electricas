# from ui.kivy_interfaz_v3 import MyApp

# if __name__ == '__main__':
#     app = MyApp();
#     app.run()

# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager

# from ui.screen0_loading import Screen0_loading
# from ui.screen1 import Screen1
# from ui.screen2 import Screen2
# from ui.screen3 import Screen3
# from ui.screen2_modulation import Screen2_modulation

# class MyApp(App):
#     def build(self):
#         screen_manager = ScreenManager()
#         screen_manager.add_widget(Screen0_loading(name='pantalla0'))
#         screen_manager.add_widget(Screen1(name='pantalla1'))
#         screen_manager.add_widget(Screen2(name='pantalla2'))
#         screen_manager.add_widget(Screen2_modulation(name='Screen2_modulation'))
#         screen_manager.add_widget(Screen3(name='pantalla3'))
#         return screen_manager


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ui.screen0_loading import Screen0_loading

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen0_loading(name='pantalla0'))
        
        return sm

# if __name__ == '__main__':
#     MyApp().run()



if __name__ == '__main__':
    
    import time
    t0 = time.time()
    MyApp().run()
    print(f"[INFO] Tiempo total: {time.time() - t0:.2f} segundos")


# if __name__ == '__main__':
#     MyApp().run()
