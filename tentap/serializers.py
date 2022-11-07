from rest_framework import serializers
from tentap.models import User


# https://www.django-rest-framework.org/tutorial/1-serialization/

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_admin', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        print(password)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        # return User.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.id = validated_data.get('id', instance.id)
    #     instance.user_name = validated_data.get('user_name', instance.user_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.save()
    #     return instance

# class TokensSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tokens
#         fields = ['id', 'user_name', 'access_token', 'refresh_token']
#
#     def create(self, validated_data):
#         return Tokens.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.user_name = validated_data.get('user_name', instance.user_name)
#         instance.access_token = validated_data.get('access_token', instance.access_token)
#         instance.refresh_token = validated_data.get('refresh_token', instance.refresh_token)
#         instance.save()
#         return instance
