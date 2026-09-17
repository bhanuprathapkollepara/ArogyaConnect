from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .models import User


# =========================================================
# SIGNUP
# =========================================================

def signup(request):

    # Handle GET request
    # Display the signup page
    if request.method == "GET":
        return render(
            request,
            "account/signup.html"
        )

    # Handle POST request
    # Process the signup form submitted by the user
    if request.method == "POST":

        # Get form data from the frontend
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name") or None
        last_name = request.POST.get("last_name")
        date_of_birth = request.POST.get("date_of_birth")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        location = request.POST.get("location")
        pincode = request.POST.get("pincode")
        password = request.POST.get("password")

        # -------------------------------------------------
        # Check whether email already exists
        # -------------------------------------------------

        if User.objects.filter(email=email).exists():

            return render(
                request,
                "account/signup.html",
                {
                    "error": "Email already exists"
                }
            )

        # -------------------------------------------------
        # Check whether mobile number already exists
        # -------------------------------------------------

        if User.objects.filter(
            mobile_number=mobile_number
        ).exists():

            return render(
                request,
                "account/signup.html",
                {
                    "error": "Mobile number already exists"
                }
            )

        # -------------------------------------------------
        # AUTOMATIC USERNAME CREATION
        # -------------------------------------------------

        # Remove extra spaces and convert last name
        # to lowercase
        last_name_clean = last_name.strip().lower()

        # date_of_birth comes from HTML as:
        # YYYY-MM-DD
        #
        # Example:
        # 2003-10-29
        #
        # [:4] extracts:
        # 2003
        birth_year = date_of_birth[:4]

        # Create the basic username
        #
        # Example:
        # last_name = kollepara
        # birth_year = 2003
        #
        # username = kollepara2003
        base_username = f"{last_name_clean}{birth_year}"

        # Initially use the base username
        username = base_username

        # Counter used if the username already exists
        counter = 1

        # -------------------------------------------------
        # CHECK USERNAME UNIQUENESS
        # -------------------------------------------------

        # Continue checking until we find an unused username
        while User.objects.filter(
            username=username
        ).exists():

            # Example:
            # kollepara2003
            # kollepara20031
            # kollepara20032
            # kollepara20033
            username = f"{base_username}{counter}"

            counter += 1

        # -------------------------------------------------
        # HASH PASSWORD
        # -------------------------------------------------

        # Never store the user's original password
        # directly in the database.
        #
        # make_password() converts the password into
        # a secure hashed password.
        hashed_password = make_password(password)

        # -------------------------------------------------
        # CREATE USER OBJECT
        # -------------------------------------------------

        user = User(

            # Automatically generated username
            username=username,

            # User information
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            date_of_birth=date_of_birth,

            # Contact information
            email=email,
            mobile_number=mobile_number,
            location=location,
            pincode=pincode,

            # Store hashed password
            password=hashed_password
        )

        # -------------------------------------------------
        # SAVE USER TO DATABASE
        # -------------------------------------------------

        user.save()

        # After successful signup,
        # redirect the user to the login page
        return redirect("login")


# =========================================================
# LOGIN
# =========================================================

def login(request):

    # Handle GET request
    # Display the login page
    if request.method == "GET":
        return render(
            request,
            "account/login.html"
        )

    # Handle POST request
    # Process login form
    if request.method == "POST":

        # Get login input and password from frontend
        # The user can enter username, mobile number, or email
        login_input = request.POST.get("login_input")
        password = request.POST.get("password")

        try:

            # Find the user using:
            # 1. Username
            # 2. Mobile number
            # 3. Email address
            user = User.objects.get(
                Q(username=login_input) |
                Q(mobile_number=login_input) |
                Q(email=login_input)
            )

            # Compare the entered password with
            # the hashed password stored in database
            if check_password(
                password,
                user.password
            ):

                # Create a session after successful login
                request.session["user_id"] = user.id

                # Store username in session
                request.session["username"] = user.username

                # Redirect the user to dashboard
                return redirect("dashboard")

            # Password does not match
            return render(
                request,
                "account/login.html",
                {
                    "error": "Invalid password",
                    "login_input": login_input
                }
            )

        # Username, mobile number, or email does not exist
        except User.DoesNotExist:

            return render(
                request,
                "account/login.html",
                {
                    "error": "Username, mobile number, or email does not exist",
                    "login_input": login_input
                }
            )

        # This can happen if multiple records match
        except User.MultipleObjectsReturned:

            return render(
                request,
                "account/login.html",
                {
                    "error": "Multiple accounts found. Please contact support.",
                    "login_input": login_input
                }
            )

# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):
    # Get logged-in user's ID from session
    user_id = request.session.get("user_id")

    # If there is no session,
    # user is not logged in
    if not user_id:
        return redirect("login")

    try:

        # Get the user from database
        user = User.objects.get(
            id=user_id
        )

        # Send user information to dashboard template
        return render(
            request,
            "dashboard/dashboard.html",
            {
                "user": user
            }
        )

    # If the user no longer exists in database
    except User.DoesNotExist:

        # Clear the invalid session
        request.session.flush()

        # Send user back to login page
        return redirect("login")


# =========================================================
# LOGOUT
# =========================================================

def logout(request):

    # Remove all session data
    request.session.flush()

    # Redirect user to login page
    return redirect("login")