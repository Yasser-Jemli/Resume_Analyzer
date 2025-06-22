package org.example.Cv_Parser.Core.exceptions;

public class CustomExceptions {

    public static class ManagerNotFoundException extends RuntimeException {
        public ManagerNotFoundException(String email) {
            super("Manager not found with email: " + email);
        }
    }

    public static class InvalidCurrentPasswordException extends RuntimeException {
        public InvalidCurrentPasswordException() {
            super("Current password is incorrect");
        }
    }

}
