# fish_captures_dev
Development repo for a mobile/web app to record fish captures with a single button press



## `forms.py` 

The `forms.py` module contains the form classes used in the application. These forms facilitate user interactions such as logging in, registering, and recording fish captures. The module leverages the Flask-WTF extension to simplify form creation and validation.

### Classes:

#### `LoginForm`
- **Purpose**: Form for users to log in.
- **Fields**:
  - `username`: A required field for the user's username.
  - `password`: A required field for the user's password.
  - `remember_me`: A checkbox to remember the user's session.
  - `submit`: A button to submit the form.

#### `RegistrationForm`
- **Purpose**: Form for new users to register.
- **Fields**:
  - `username`: A required field for the user's desired username.
  - `email`: A required field for the user's email address, validated for proper email format.
  - `password`: A required field for the user's desired password.
  - `password2`: A required field to confirm the user's password. Must match the first password field.
  - `submit`: A button to submit the form.
- **Custom Validations**:
  - `validate_username`: Ensures the provided username is unique and not already in use.
  - `validate_email`: Ensures the provided email address is unique and not already in use.

#### `FishCaptureForm`
- **Purpose**: Form for users to record details of a fish capture.
- **Fields**:
  - `GPS_location`: A required field for the GPS location of the fish capture.
  - `fishing_spot_tag`: A required field for tagging the fishing spot.
  - `tide_state`: A required field for the tide state during the capture.
  - `weather_conditions`: A required field for the weather conditions during the capture.
  - `daylight_state`: A required field for the daylight state (e.g., dawn, midday, dusk) during the capture.
  - `fish_type`: A required field for the type/species of fish captured.
  - `lure_bait_type`: A required field for the type of lure or bait used.
  - `submit`: A button to submit the form.

### Usage:

To use these forms in the application, instantiate the desired form class and render it in the appropriate template. The forms come with built-in validation methods that can be invoked using the `validate_on_submit()` method.


## Database Models

### User

This model represents registered users of the application.

- **Attributes**:
  - `id`: Unique identifier for the user.
  - `username`: Unique username for the user.
  - `email`: Unique email address for the user.
  - `password_hash`: Hashed version of the user's password.
  - `date_joined`: Timestamp indicating when the user joined.

- **Relationships**:
  - `fish_captures`: List of fish captures associated with the user.
  - `user_preferences`: User's preferences.

- **Methods**:
  - `set_password(password)`: Sets the hashed version of the given password to the user.
  - `check_password(password)`: Checks if the given password matches the stored hashed password.

### FishCapture

This model represents the details of a fish capture event.

- **Attributes**:
  - `id`: Unique identifier for the fish capture event.
  - `user_id`: Foreign key referencing the associated user.
  - `timestamp`: Timestamp of the fish capture event.
  - `GPS_location`: GPS location where the fish was captured.
  - `fishing_spot_tag`: Tag or name of the fishing spot.
  - `tide_state`: State of the tide during the capture.
  - `weather_conditions`: Weather conditions during the capture.
  - `daylight_state`: Daylight conditions (e.g., dawn, day, dusk, night).
  - `fish_type`: Type or species of the captured fish.
  - `lure_bait_type`: Type of lure or bait used.

### UserPreferences

This model represents the user's preferred settings and options.

- **Attributes**:
  - `id`: Unique identifier for the user preferences.
  - `user_id`: Foreign key referencing the associated user.
  - `fish_button_1`: First customizable fish button.
  - `fish_button_2`: Second customizable fish button.
  - `fish_button_3`: Third customizable fish button.
  - `lure_bait_options`: Customizable lure/bait options.

