from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
# registration with only username and pass1 and pass2 won't work and raised an error that said 
# " user got unexpected argument password2 so we added the email and firstname last names fields and it work we will come back after 

# from .models import CustomUser
# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'last_login', 'date_joined', 'is_staff')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    group = serializers.CharField(required=True)
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('password', 're_password', 'email', 'first_name', 'last_name', 'group')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        group = Group.objects.get(name=validated_data['group']) 
        print(' THE GROUP', group)
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active =True,
            is_staff =True
        )

        user.set_password(validated_data['password'])
        user.groups.add(group)
        user.save()
        return user



class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    get_first_group = serializers.SerializerMethodField("get_left_minutes", read_only=True)
    class Meta:
        model = User
        fields = "__all__"
        # fields = ('id', 'email', 'groups', 'get_first_group', 'first_name', 'last_name',)
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True},
        # }

    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # def validate_username(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value
    def get_first_group(self, obj):
        return obj.get_first_group()
    def update(self, instance, validated_data):
        user = self.context['request'].user
        # if user.pk != instance.pk:
        #     raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        print('What received', validated_data['groups'])
        groups = validated_data['groups']
        group = groups[0]
        print('INSTRANCE GRTOUSP BEFORE', type(instance))
        print('Groups after', group)
        groups = instance.groups.set([group])
        print('Final groups after', groups)

        instance.save()
        return instance

 
class ReadUsersView(serializers.ModelSerializer):
    # client = serializers.CharField(source = "abc.client")
    get_first_group = serializers.SerializerMethodField("first_group_name", read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'groups', 'get_first_group', 'first_name', 'last_name',)
        # fields = "__all__"

        # read_only_fields = 'username'
    def first_group_name(self, obj):
        group = obj.groups.first() 
        if group :
            return group.name
        else:
            return ""
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        # read_only_fields = 'username'

class ObtainTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
