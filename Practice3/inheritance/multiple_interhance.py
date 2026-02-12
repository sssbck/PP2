class Logger:
    def log(self, message: str):
        print("[LOG]", message)

class Saver:
    def save(self, data: str):
        print("[SAVE]", data)

class App(Logger, Saver):
    def run(self):
        self.log("App started")
        self.save("user_settings.json")
        self.log("App finished")

if __name__ == "__main__":
    app = App()

    app.log("Hello")

    app.save("data.txt")

    app.run()

    print("MRO:", [cls.__name__ for cls in App.mro()])
