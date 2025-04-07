from static import Static
from utils import resource_path

import os

class Start:
    def excute(self, status, event):
        from button import Button, click_start, click_end
        # start button
        status.items["start-button"] = Button(pos=[status.screen.get_width() / 2, 
                                        status.screen.get_height() / 2 - 60, 1],
                    json_path=resource_path("./configs/buttons/start_button.json"),
                    on_click=click_start,
                    name="start-button")
        # end button
        status.items["end-button"] = Button(pos=[status.screen.get_width() / 2, 
                                        status.screen.get_height() / 2 + 60, 1],
                    json_path=resource_path("./configs/buttons/end_button.json"),
                    on_click=click_end,
                    name="end-button")
        # logo
        status.items["logo"] = Static(pos=[status.screen.get_width() / 2,
                                       status.screen.get_height() / 2 - 180, 1],
                    json_path=resource_path("./configs/statics/logo.json"),
                    name="logo")
        return False