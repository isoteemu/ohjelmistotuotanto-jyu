class Project:
    def __init__(self, name, description, license, authors, dependencies, dev_dependencies):
        self.name = name
        self.description = description
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies
        self.license = license
        self.authors = authors if isinstance(authors, list) else [authors]
        

    def _stringify_dependencies(self, dependencies):
        return "\n- ".join(dependencies) if len(dependencies) > 0 else ""

    def __str__(self):
        return (
            f"Name: {self.name}"
            f"\nDescription: {self.description or '-'}"
            f"\nLicense: {self.license or '-'}\n"
            f"\nAuthors:\n- {self._stringify_dependencies(self.authors)}\n"
            f"\nDependencies:\n- {self._stringify_dependencies(self.dependencies)}\n"
            f"\nDevelopment dependencies:\n- {self._stringify_dependencies(self.dev_dependencies)}\n"
        )
