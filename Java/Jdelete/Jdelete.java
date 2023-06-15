import java.io.File;
import java.nio.file.Path;
import java.nio.file.Files;
import java.io.IOException;

public class Jdelete{
	public static void main(String[] args){
		Runnable r = new MyRun();
		Thread t = new Thread(r);
		t.start();
	}
	
	public static String readFile(String filename) throws IOException {
        File file = new File(filename);
        String content = "";
        if (file.exists() && file.isFile()) {
            content = Files.readString(Path.of(filename));
        } else {
            System.out.println("settings.ini is not exist!");
        }
        return content;
    }
	
}

class MyRun implements Runnable{
	public void run(){
		try {
			String[] dirs = Jdelete.readFile("settings.ini").split("\n");
			for (String dir : dirs){
				System.out.println("delete: " + dir);
				File file = new File(dir);
				delete(file);
			}
		}catch (IOException e) {
			System.out.println("settings.ini is not exist!");
		}
	}
	
	public static void delete(File file){
		if (file.isDirectory()){
			File[] files = file.listFiles();
			for(File _file : files){
				delete(_file);
			}
			file.delete();
		}else{
			file.delete();
		}
	}
}