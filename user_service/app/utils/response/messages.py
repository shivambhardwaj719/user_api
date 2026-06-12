class ResponseMessages:
    VALID_WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    SUCCESS = "Success"
    WARNING = "Warning"
    BAD_REQUEST = "Bad Request"
    UNAUTHORIZED = "Authentication credentials required."
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    NOT_REGISTERED_USER = "User not registered"
    FORBIDDEN = "Insufficient permissions to access this resource."
    NOT_FOUND = "Not Found"
    TOO_MANY_REQUESTS = "Too Many Requests"
    SERVER_ERROR = "Server Error"
    CREATE_FAILED = "creation failed."
    DELETE_FAILED = "deletion failed."
    UPDATE_FAILED = "update failed."
    VALIDATION_ERROR = "Validation error."
    UNEXPECTED_ERROR = "Unexpected error occurred."
    NO_MATCHING_DATA = "No matching data found."
    PASSWORD_MISMATCH = "Passwords don't match"
    INVALID_TOKEN = "Invalid or expired token"
    EMAIL_ALREADY_IN_USE = "Email already in use. Please use a different one."
    PHONE_ALREADY_IN_USE = "Phone number already in use."
    PASSWORD_UPDATED = "Password updated"
    PASSWORD_EMAIL_SENT = "Password reset email sent successfully."
    USER_CREATION_EMAIL_NOTICE = "User created. Please check email to set password."
    STAFF_NOT_FOUND = "Staff not found"
    PERMISSION_NOT_FOUND = "Permission with ID {id} not found."
    NO_PERMISSIONS_PROVIDED = "No permission IDs provided for assignment or removal."
    PERMISSION_ASSIGN_SUCCESS = "Permissions updated successfully."
    USER_PERMISSIONS_FETCH_SUCCESS = "User permissions fetched successfully."
    USER_NOT_FOUND = "User not found."
    NO_IDS_PROVIDED = "No IDs provided for deletion."
    GROUP_CONNECTED = "Group '{group_name}' is connected to a user and cannot be deleted."
    ADMIN_GROUP_CANNOT_BE_DELETED = "Admin group cannot be deleted."
    NO_PERMISSIONS_OR_NAME_PROVIDED = "No permissions or group name provided for assignment, removal, or update."
    GROUPS_REQUIRED = "'groups' required in request body."
    GROUP_ID_AND_ACTION_REQUIRED = "Group IDs and action required for each group."
    INVALID_ACTION = "Invalid action. Use 'enable' or 'disable'."
    GROUP_UPDATE_SUCCESS = "User '{user_id}' updated with groups {group_ids}."
    GROUP_NOT_FOUND = "Group not found."
    USER_ALREADY_EXISTS = "User already exists with name: {name}."
    MISSING_EMAIL_FOR_STAFF_USER = "Email required to create user from staff."
    NEW_USER_CREATED_TITLE = "New User Created"
    NEW_USER_CREATED_BODY = "A new user '{name}' has been registered."
    NEW_STAFF_USER_CREATED_TITLE = "New Staff User Created"
    NEW_STAFF_USER_CREATED_BODY = "A new user '{name}' was created via the Staff portal."


    @staticmethod
    def no_permission():
        return ResponseMessages.NO_PERMISSION

    @staticmethod
    def create_success_message(name: str):
        return f"{name} added successfully."

    @staticmethod
    def update_success_message(name: str):
        return f"{name} updated successfully."

    @staticmethod
    def delete_success_message(count: int):
        return f"{count} deleted successfully."
    
    @staticmethod
    def not_found(name: str):
        return f"{name} not found"
    
    @staticmethod
    def partial_delete_message(connected_staffs: any):
        return "Some were deleted, but some could not be deleted due to existing connections."

    @staticmethod
    def none_deleted_message(connected_staffs: any):
        return "No were deleted."

    @staticmethod
    def validation_error_message():
        return "Validation error."

    @staticmethod
    def field_required(field):
        return f"{field} field is required"
    