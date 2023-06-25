import java.util.Random;

public class Utility {
    private static Utility instance = new Utility();
    private Utility(){}
    public static Utility getInstance() { return instance; }

    private Random rand = new Random();

    public int randomValue(){
        return Settings.VALUES[rand.nextInt(Settings.VALUES.length)];
    }
    
}
