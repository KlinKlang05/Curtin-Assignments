package edu.curtin.citybuilder.gridunit;

public class InvalidHeritageException extends Exception {
    public InvalidHeritageException(String msg) {
        super(msg);
    }

    public InvalidHeritageException(String msg, Throwable cause) {
        super(msg, cause);
    }

    public InvalidHeritageException(Throwable cause) {
        super(cause);
    }
}
