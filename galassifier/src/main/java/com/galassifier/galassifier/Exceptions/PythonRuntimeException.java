package com.galassifier.galassifier.Exceptions;

public class PythonRuntimeException extends RuntimeException {
    public PythonRuntimeException(String message) {
        super(message);
    }

    public String getPythonRuntimeErrorMessage()
    {
        return super.getMessage();
    }
}
