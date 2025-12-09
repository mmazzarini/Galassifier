package com.galassifier.galassifier.Utilities;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

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


    public static StringBuilder HandleStdInput(Process process)  
    {   
        StringBuilder output = new StringBuilder();
        try(BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()) )){
            String line;
            while ((line = reader.readLine()) != null){
                output.append(line).append(System.lineSeparator());
            }
        }
        catch (IOException e){
            throw new RuntimeException("[HandleStdInput] Cannot read process log with output error: " + e);
        }

        return output;
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
