import importlib.metadata

__version__ = importlib.metadata.version("social-auth-app-django")


from social_core.backends.base import BaseAuth

# django.contrib.auth.load_backend() will import and instantiate the
# authentication backend ignoring the possibility that it might
# require more arguments. Here we set a monkey patch to
# BaseAuth.__init__ to ignore the mandatory strategy argument and load
# it.


def baseauth_init_workaround(original_init):
    def fake_init(self, strategy=None, *args, **kwargs):
        from .utils import load_strategy  # noqa: PLC0415

        original_init(self, strategy or load_strategy(), *args, **kwargs)

    return fake_init


if not getattr(BaseAuth, "__init_patched", False):
    BaseAuth.__init__ = baseauth_init_workaround(BaseAuth.__init__)  # type: ignore[method-assign]
    BaseAuth.__init_patched = True  # type: ignore[attr-defined] # noqa: SLF001
