from django.contrib.auth import get_user_model

User = get_user_model()

def EmailAuth(email, password):
    try:
        print(f"Attempting to authenticate user with email: {email}")
        user = User.objects.get(email=email)
        print(f"User found: {user.first_name} {user.last_name}")
        print(f"User is active: {user.is_active}")

        if user.check_password(password):
            print("Password check successful")
            return user
        else:
            print("Password check failed")
            return None
    except User.DoesNotExist:
        print(f"User with email {email} does not exist")
        return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
