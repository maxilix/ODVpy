import dearpygui.dearpygui as dpg
from PIL.ImageOps import scale

dpg.create_context()

width, height, channels, data = dpg.load_image("./extracted/maps/00.bmp")
with dpg.texture_registry(show=False):
    texture_id = dpg.add_static_texture(width, height, data)


zoom = 1.0
zoom_factor = 1.25


def zoom_callback(sender, app_data, user_data):
    global zoom

    if app_data > 0:
        zoom *= zoom_factor
    elif app_data < 0:
        zoom /= zoom_factor

    # Appliquer le zoom en redimensionnant l'image
    new_width = int(width * zoom)
    new_height = int(height * zoom)
    dpg.configure_item("zoomable_image", width=new_width, height=new_height)



with dpg.window(label="Map View", width=1400, height=1000, no_scrollbar=True, no_scroll_with_mouse=True, no_close=True):
    with dpg.handler_registry():
        dpg.add_mouse_wheel_handler(callback=zoom_callback)
    dpg.add_image(texture_id, tag="zoomable_image")



dpg.create_viewport(title='ODVpy-dpg')
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
