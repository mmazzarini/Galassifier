package com.galassifier.galassifier.Utilities;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import com.galassifier.galassifier.Exceptions.PythonRuntimeException;

public class GalassifierProcessLibrary {
    
    public static Process HandleStartProcess(ProcessBuilder pB)
    {
        Process process = null;
        try {
            process = pB.start();
        } catch (IOException e) {
            throw new PythonRuntimeException("Could not find process...");
        }
        
        return process;
    }


    public static BufferedReader HandleStdInput(Process process)  
    {   
        BufferedReader stdInput = null;
        if(process != null)
        {
            stdInput = new BufferedReader(
            new InputStreamReader(process.getInputStream()));
        }
        return stdInput;
    }

    public static int HandleWaitForProcess(Process process)
    {
        int exitCode = 0;
        try {
            exitCode = process.waitFor();
        } catch(InterruptedException e) {
            System.out.println("got interrupted!");
        }
        return exitCode;
    }

    public static String HandleInputRead(BufferedReader stdInput) 
    {
        String galaxyTypeString = "";
        try {
            galaxyTypeString = stdInput.readLine();
        } catch (IOException e) {
            throw new PythonRuntimeException("Could not read process output...");
        }
        return galaxyTypeString;
    }

    public static void HandleInputClose(BufferedReader stdInput)
    {
        try {
            stdInput.close();
        } catch (IOException e) {
            throw new PythonRuntimeException("Could not close process output...");
        }
    }

    public static String HandleErrorInput(Process process)
    {
        StringBuilder errorOutput = new StringBuilder();
        try (BufferedReader errorReader = new BufferedReader(
                new InputStreamReader(process.getErrorStream()))) {
            String line;
            while ((line = errorReader.readLine()) != null) {
                errorOutput.append(line).append("\n");
            }
        } catch (IOException e) {
            throw new PythonRuntimeException("Could not read error output...");
        }
        return errorOutput.toString();
    }

}
