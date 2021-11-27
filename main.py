import yaml, os, click

class Autobrew_Homebrew:
    def __init__(self, config, categories=None):
        self._configFile = config
        self._configBody  = open(self._configFile)
        self.config = yaml.safe_load(self._configBody)
        if not categories:
            self.categories = ["core", "cask"]

    def _installBrewList(self, category):
        print(f"Starting install of {self._configFile} version {self.config['version']}")
        if category == "cask":
            __prefix = "brew install --cask "
        else:
            __prefix = "brew install "
        for LineItem in self.config[category]:
            os.system(__prefix + LineItem)
    
    def runDryRunReport(self):
        returnBody = ""
        for category in self.categories:
            returnBody += f"\nCategory: {category} (contains {len(self.config[category])} packages)\n"
            for LineItem in self.config[category]:
                returnBody += f"Package: {LineItem}\n"
        return returnBody
    
    def runYamlInstall(self):
        for category in self.categories:
            x = self._installBrewList(category)

@click.group()
def main():
    pass

@main.command()
@click.option("--file", prompt="Specifiy path to your YAML file", type=str)
@click.option("--confirm", type=bool)
def install(file, confirm):
    Autobrew = Autobrew_Homebrew(file)
    if confirm:
        Autobrew.runYamlInstall()
    else:
        print(Autobrew.runDryRunReport())


if __name__ == "__main__":
    main()
