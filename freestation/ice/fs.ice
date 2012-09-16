// #include <Process.ice>
//[["python:package:zeroc"]]
[["cpp:include:list"]]
module FS {
   class Example {
     short apilevel; // Version for this API
   };
   
   const int lambda = 0;
   
   sequence<string> StringSeq;
    dictionary<string, string> StringDict;
   
   
   struct mystruct
   {
     int mytype;
     
         bool bo;
    byte by;
    short sh;
    int i;
    long l;
    float f;
    double d;
    string str;
    StringSeq ss;
    StringDict sd;
    Example s;
    Object* prx;
     
   };
   
   enum EnumNone {
        None
    };
   
   exception myexcep
    {
        int lambda;
    };
   
    //interface FileSender
    //{
    //    int getFileSize(string path);
    //    
    //};
   
   sequence<byte> File;
   sequence<byte> FileBlock;
   
   interface Api {
     void getWidgets();
     string getXMLWidgets();
     void version(out string sout);
     int getFileSize(string path);
     File getFile(string path);
     FileBlock getFileChunk(string path, int pos, int size);
     void isAuthorized(out bool sout);
     int getClientId();
   };
   interface Widget 
   {
     void getName();
   };
   
   exception GenericError {
     string reason;
   };
   exception NoAuthorized extends GenericError {};
};