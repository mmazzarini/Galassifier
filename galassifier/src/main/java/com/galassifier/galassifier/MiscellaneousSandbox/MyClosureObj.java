package com.galassifier.galassifier.MiscellaneousSandbox;

import java.io.Closeable;

// Simple class to test the Closeable interface and try-with-resources statement

public class MyClosureObj implements Closeable{
    @Override
    public void close(){
        System.out.println("[[TERMINATE]] MyClosureObj is closing!");
    }

    public void gooGoo()
    {
        System.out.println("[[MyClosureObj]] GaaGaa!");
    }
}
