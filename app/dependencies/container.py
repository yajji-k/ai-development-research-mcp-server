from app.config.settings import Settings, get_settings


class Container:
    @property
    def settings(self) -> Settings:
        return get_settings()
