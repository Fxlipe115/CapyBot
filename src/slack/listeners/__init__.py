from slack_bolt import App


class Listeners:
    app: App
    def __init__(self, app: App) -> None:
        self.app = app

    def register_event(self):
        self.app.event