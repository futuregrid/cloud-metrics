class FGTester:

    def run(self):
        self.check_config()
        self.check_database()
        self.check_functions() #?
        self.check_graphs() #?
        self.check_webpages() #?
        self.check_crontabs() #?

if __name__ == "__main__":
    main = FGTester()
    main.run()
