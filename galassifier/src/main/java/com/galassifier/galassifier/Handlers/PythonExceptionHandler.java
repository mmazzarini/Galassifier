package com.galassifier.galassifier.Handlers;

import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import com.galassifier.galassifier.Exceptions.PythonRuntimeException;

@ControllerAdvice
public class PythonExceptionHandler {
    // You can implement exception handling methods here

    @ExceptionHandler(PythonRuntimeException.class)
    public void handlePythonRuntimeException(PythonRuntimeException e)
    {
        System.out.println("[PythonExceptionHandler]:: Handled PythonRuntimeException, with error msg: ' %s '" + e.getPythonRuntimeErrorMessage());
    }
}

