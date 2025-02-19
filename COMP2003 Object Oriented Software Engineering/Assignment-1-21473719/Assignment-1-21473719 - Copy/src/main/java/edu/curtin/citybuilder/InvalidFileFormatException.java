package edu.curtin.citybuilder;

public class InvalidFileFormatException extends Exception {
    public InvalidFileFormatException(String msg) {
        super(msg);
    }

    public InvalidFileFormatException(String msg, Throwable cause) {
        super(msg, cause);
    }

    public InvalidFileFormatException(Throwable cause) {
        super(cause);
    }
}
