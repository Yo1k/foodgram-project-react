from rest_framework.serializers import ValidationError


class FavoriteActionError(ValidationError):
    pass


class SubscribeActionError(ValidationError):
    pass
